from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag, Comment
from .forms import CommentForm, PostSearchForm

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    search_form = PostSearchForm(request.GET)
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )
        if category:
            posts = posts.filter(category=category)
    
    paginator = Paginator(posts, 9)  # 9 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'search_form': search_form,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, is_published=True)
    post.views_count += 1
    post.save()
    
    # Related posts
    related_posts = Post.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id)[:3]
    
    # Comments
    comments = post.comments.filter(is_approved=True, parent_comment__isnull=True)  # Only top-level comments
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            parent_comment_id = request.POST.get('parent_comment_id')  # Get parent comment ID
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                comment.parent_comment = parent_comment
            comment.save()
            messages.success(request, 'تم إضافة تعليقك بنجاح وسيتم مراجعته')
            return redirect('blog:post_detail', post_slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

def post_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, is_published=True)
    
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'blog/post_by_category.html', {
        'category': category,
        'posts': posts,
    })

def post_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag, is_published=True)
    
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'blog/post_by_tag.html', {
        'tag': tag,
        'posts': posts,
    })

@login_required
def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            parent_comment_id = request.POST.get('parent_comment_id')  # Get parent comment ID
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                comment.parent_comment = parent_comment
            comment.save()
            messages.success(request, 'تم إضافة تعليقك بنجاح وسيتم مراجعته')
    return redirect('blog:post_detail', post_slug=post.slug)

@login_required
def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    # إذا كان المستخدم قد أعجب بالمنشور مسبقًا، قم بإزالته
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.success(request, 'تم إزالة إعجابك بالمنشور.')
    else:
        # إذا كان المستخدم قد كره المنشور مسبقًا، قم بإزالته من الكره وإضافته إلى الإعجابات
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
        messages.success(request, 'تم تسجيل إعجابك بالمنشور.')
    
    return redirect('blog:post_detail', post_slug=post.slug)

@login_required
def dislike_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    # إذا كان المستخدم قد كره المنشور مسبقًا، قم بإزالته
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        messages.success(request, 'تم إزالة كرهك للمنشور.')
    else:
        # إذا كان المستخدم قد أعجب بالمنشور مسبقًا، قم بإزالته من الإعجابات وإضافته إلى الكره
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
        messages.success(request, 'تم تسجيل كرهك للمنشور.')
    
    return redirect('blog:post_detail', post_slug=post.slug)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Comment
from .forms import CommentForm

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # التحقق من أن المستخدم هو صاحب التعليق
    if comment.user != request.user:
        messages.error(request, 'ليس لديك صلاحية لتعديل هذا التعليق.')
        return redirect('blog:post_detail', post_slug=comment.post.slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.is_edited = True  # تم تعيينه تلقائيًا إلى True
            comment.save()
            messages.success(request, 'تم تعديل التعليق بنجاح!')
            return redirect('blog:post_detail', post_slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'blog/edit_comment.html', context)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # التحقق من أن المستخدم هو صاحب التعليق
    if comment.user != request.user:
        messages.error(request, 'ليس لديك صلاحية لحذف هذا التعليق.')
        return redirect('blog:post_detail', post_slug=comment.post.slug)
    
    comment.delete()
    messages.success(request, 'تم حذف التعليق بنجاح!')
    return redirect('blog:post_detail', post_slug=comment.post.slug)