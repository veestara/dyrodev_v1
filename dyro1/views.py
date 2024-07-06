from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import *
from django.urls import reverse
from .forms import CategoryForm, PostForm
import logging
from .forms import *
import random
from django.http import JsonResponse

logger = logging.getLogger(__name__)
  

def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    subject = 'OTP Verification - Dyro Dev'
    message = f'Howdy! Your OTP for Dyro Dev registration is: {otp}'
    from_email = 'verify.dyrodev@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


# ------------------------------------------------------
    # 20/06/2024
def home(request):
    if request.method == 'POST':
        name = request.POST.get('fullName')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if email:
        # Save the form data to the database
            Contact.objects.create(name=name, phone=phone, email=email, message=message)
            
            user_subject = 'Thank You for Contacting Dyro Dev!'
            user_message_body = f'''
Dear {name},

Thank you for reaching out to us! We have received your message and appreciate you taking the time to contact us.

Our team is reviewing your inquiry and will get back to you as soon as possible. In the meantime, if you have any additional information or questions, please feel free to reply to this email.

Best regards,
Dyro Dev
'''

            user_sender_email = settings.EMAIL_HOST_USER
            
            send_mail(user_subject, user_message_body, user_sender_email, [email])
        
            # Prepare the email
            subject = f'Contact Form Submission from {name}'
            message_body = f'Name: {name}\nPhone: {phone}\nEmail: {email}\n\nMessage:\n{message}'
            sender_email = settings.EMAIL_HOST_USER
            recipient_email = 'info.dyrodev@gmail.com'  # Replace with your email address
                        
            send_mail(subject, message_body, sender_email, [recipient_email])
            
            return render(request, 'success.html')
        
        try:
            # Send email
            send_mail(
                subject,
                message_body,
                sender_email,
                [recipient_email],
                fail_silently=False,
            )
            return redirect('success')  # Redirect to a success page
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return redirect('error')  # Redirect to an error page
        
    return render(request, "index.html")

# ------------------------------------------------------


def about(request):
    return render(request, "about.html")


def sunpac_view(request):
    return render(request, "sunpac-view.html")


def work(request):
    return render(request, "work-view.html")

# Authentication-------------------------------------------------------------------


def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hpss = make_password(password)
        request.session['registration_email'] = email
        
        if User.objects.filter(email=email).exists():
            msg = "Email is already registered"
            return render(request, 'auth/signup.html', {'msg': msg})
    
        email_otp = generate_otp()
        
        request.session['registration_data'] = {
            'first_name': fname,
            'last_name': lname,
            'phone': phone,
            'email': email,
            'password': hpss,  # Hash the password
            'email_otp': email_otp
        }
        
        with transaction.atomic():
            request.session['email_otp'] = email_otp

            # Send OTPs to user's email and phone
            send_otp_email(email, email_otp)

        return redirect('otp')
    
    return render(request, 'auth/signup.html')


def login(request):
    
    if request.method == 'POST':
        mail = request.POST.get('email') 
        password = request.POST.get('password')

        if not mail or not password:
            msg = '~ Incomplete Form '
            return render(request, "auth/login.html", {'msg': msg})

        try:
            user = User.objects.get(email=mail)
        except User.DoesNotExist:
            msg = '~ No user found'
            return render(request, "auth/login.html", {'msg': msg})
      
        print(f'User hashed password: {user.password}')

        if not check_password(password, user.password):
            msg = 'Invalid password'
            return render(request, "auth/login.html", {'msg': msg})
          
        else:
            request.session['is_authenticated'] = True
            request.session['user_id'] = user.id
            request.session['is_admin'] = user.is_admin
            msg = 'Login successful'
            return redirect(home)
    
    return render(request, 'auth/login.html')


def logout(request):
    request.session['is_authenticated'] = False
    request.session['is_admin'] = False
    return redirect(login) 


def login_required(view_func):

    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_authenticated', False):
            return redirect(login) 
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def admin_required(view_func):

    def _warapped_view(request, *args, **kwargs):
        if not request.session.get('is_admin', False):
            return redirect(login)
        return view_func(request, *args, **kwargs)

    return _warapped_view 


def forget(request):
    
    msg = ''

    if request.method == "POST":
        email = request.POST.get('email')
        request.session['forget_mail'] = email  # Storing email in session

        try:
            user = User.objects.get(email=email)

            if user:
                otp = generate_otp()
                request.session['fotp'] = otp  # Storing OTP in session

                with transaction.atomic():
                    # Send OTP to user's email
                    send_otp_email(email, otp)

                return redirect('otp')  # Redirect to OTP verification page
            else:
                msg = "Email is not registered"
        except ObjectDoesNotExist:
            msg = "Email is not registered"
    
    return render(request, 'auth/forget.html', {'msg': msg})


def otp(request):
    rgmail = request.session.get('registration_email')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_data = request.session.get('registration_data')
        fotp = request.session.get('fotp')
        
        # if not session_data:
        #     msg = "Please fill all fields"
        #     return render(request, 'auth/signup.html')
        
        stored_otp = request.session.get('email_otp')
        
        if entered_otp == stored_otp:
            # Save the user data to the database
            User.objects.create(
                first_name=session_data['first_name'],
                last_name=session_data['last_name'],
                phone=session_data['phone'],
                email=session_data['email'],
                password=session_data['password']
            )
            
            del request.session['email_otp']
            del request.session['registration_data']
            del request.session['registration_email']
           
            return redirect(login)
        
        elif entered_otp == fotp:
            
            del request.session['fotp']

            return redirect(reset)
        
        else:
            msg = "invalid otp"
            return render(request, 'auth/otp.html', {'msg': msg})
    
    return render(request, 'auth/otp.html', {'rgmail': rgmail})


def reset(request):
    
    if request.method == 'POST':
        npass = request.POST.get('npassword')
        cpass = request.POST.get('cpassword')
        fmail = request.session.get('forget_mail')
        
        try:
            user = User.objects.get(email=fmail)
        except User.DoesNotExist:
            msg = '~ No user found'
            return render(request, "auth/login.html", {'msg': msg})
        
        print(f'{npass}')
        print(f'{cpass}')
        
        if str(npass) == str(cpass):
            
            hpass = make_password(npass)
            
            if user:
                
                user.password = hpass
                user.save()
        
                del request.session['forget_mail']
                
                return redirect(login)
            
            else:
                
                msg = 'Email is not registered'
                return render(request, 'auth/reset.html', {'msg': msg})
            
        else:
            msg = 'Confirm password is not matching'
            return render(request, 'auth/reset.html', {'msg': msg})
    
    return render(request, 'auth/reset.html')

# ===========================================

# category


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})


def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})


def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form})


def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'category/category_detail.html', {'category': category})

# =======================================


def add_comment(request, slug):
    if not request.session.get('is_authenticated'):
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return JsonResponse({
                'name': new_comment.name,
                'body': new_comment.body,
                'created_on': new_comment.created_on.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'error': 'Invalid form data'}, status=400)



# Post views
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_grid(request):
    posts = Post.objects.all()
    return render(request, 'u-posts/post-grid.html', {'posts': posts})


def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('post_detail', kwargs={'slug': post.slug}))
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {'form': form, 'post': post})


def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    
    is_auth = request.session.get('is_authenticated', False)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'is_auth': is_auth
    })
    


# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'posts/post_detail.html', {'post': post})


# ==================================================
# video
def video_create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'videos/video_form.html', {'form': form})


def video_update(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            video = form.save()
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'videos/video_form.html', {'form': form, 'video': video})


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})


def video_grid(request):
    videos = Video.objects.all()
    return render(request, 'u-videos/video-grid.html', {'videos': videos})
    

def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        return redirect('video_list')
    return render(request, 'videos/video_confirm_delete.html', {'video': video})


def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    youtube_id = get_youtube_id_from_embed_code(video.embed_code)
    related_videos = Video.objects.filter(related_keyword=video.related_keyword).exclude(id=video.id).order_by('-id')[:5]

    return render(request, 'videos/video_detail.html', {'video': video, 'youtube_id': youtube_id, 'related_videos': related_videos})


def get_youtube_id_from_embed_code(embed_code):
    match = re.search(r'src="https://www.youtube.com/embed/([^"]+)"', embed_code)
    if match:
        return match.group(1)
    return None
