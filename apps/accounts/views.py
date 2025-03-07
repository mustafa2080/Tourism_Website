from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, FormView, RedirectView
from .forms import UserRegistrationForm, UserUpdateForm, UserLoginForm, ProfileForm, UserForm
from .models import UserProfile
from allauth.socialaccount.models import SocialApp
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings

@method_decorator(ensure_csrf_cookie, name='dispatch')
class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse('core:home')  # استخدام reverse لتوليد المسار

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'تم تسجيل حسابك بنجاح!')
        return super().form_valid(form)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse('core:home')  # استخدام reverse لتوليد المسار

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'تم تسجيل الدخول بنجاح!')
        else:
            messages.error(self.request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CSRF_COOKIE_NAME'] = settings.CSRF_COOKIE_NAME
        return context

class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('core:home')  # استخدام reverse لتوليد المسار

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'تم تسجيل الخروج بنجاح!')
        return super().get(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_bookings'] = self.request.user.booking_set.all().order_by('-created_at')
        return context

@method_decorator(csrf_protect, name='dispatch')
class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile_edit.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('accounts:profile')  # استخدام reverse لتوليد المسار

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'تم تحديث بياناتك بنجاح!')
        return super().form_valid(form)

class GoogleLoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        app = SocialApp.objects.get(provider='google')
        client_id = app.client_id
        redirect_uri = 'http://127.0.0.1:8000/accounts/google/callback/'
        scope = 'profile email'
        state = 'random_state_string'
        return f'https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}&response_type=code'

class FacebookLoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        app = SocialApp.objects.get(provider='facebook')
        client_id = app.client_id
        redirect_uri = 'http://127.0.0.1:8000/accounts/facebook/callback/'
        scope = 'email public_profile'
        state = 'random_state_string'
        return f'https://www.facebook.com/v7.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}&response_type=code'

@method_decorator(csrf_protect, name='dispatch')
class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form'] = UserForm(instance=user)
        
        if hasattr(user, 'userprofile'):
            context['profile_form'] = ProfileForm(instance=user.userprofile)
        else:
            UserProfile.objects.create(user=user)
            context['profile_form'] = ProfileForm(instance=user.userprofile)
        
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        user = request.user
        if 'user_form' in request.POST:
            user_form = UserForm(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'تم تحديث المعلومات الشخصية بنجاح!')
            else:
                messages.error(request, 'حدث خطأ أثناء تحديث المعلومات الشخصية.')

        elif 'profile_form' in request.POST:
            if hasattr(user, 'userprofile'):
                profile_form = ProfileForm(request.POST, request.FILES, instance=user.userprofile)
                if profile_form.is_valid():
                    profile_form.save()
                    messages.success(request, 'تم تحديث التفضيلات بنجاح!')
                else:
                    messages.error(request, 'حدث خطأ أثناء تحديث التفضيلات.')
            else:
                UserProfile.objects.create(user=user)
                messages.success(request, 'تم إنشاء ملف تعريف جديد وتحديث التفضيلات بنجاح!')

        return redirect('accounts:settings')