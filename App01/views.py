from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # force_str로 수정
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.db.models.query_utils import Q

from App01.models import Board
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .functions import recommend_district 
UPLOAD_DIR = 'C:/Users/it/.vscode/DJANGOWORK/upload/'

# 회원가입
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 사용자 계정을 비활성화 상태로 설정
            user.save()

            # 이메일 인증을 위한 이메일 전송
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            # 이메일 전송 후 사용자에게 안내 페이지를 보여줍니다.
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'common/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # 회원 가입 후 자동으로 로그인
        return redirect('account_activation_complete')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'환영합니다, {username}님!')
            return redirect('main03')  # 로그인 성공 시 이동할 페이지 설정
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, '로그아웃 되었습니다.')
    return redirect('main03')  # 로그아웃 후 메인 페이지로 이동

# write_form : 글쓰기 폼  
def write_form(request):
    return render(request,'board/insert.html')
                  

def home(request):
    return render(request, 'board/home.html')

def main(request):
    return render(request, 'main.html')

def main02(request):
    return render(request, 'main_02.html')

def main03(request):
    return render(request, 'main_03.html')

def base(request):
    return render(request,'base.html')

def naver_api(request):
    return render(request,'naver_api.html')

def icons_view(request):
    return render(request, 'icons.html')
 
def icons02_view(request):
    return render(request, 'icons02.html')


#insert
@csrf_exempt
def insert(request):
    #파일처리
    fname = ''
    fsize = 0
    if 'file' in request.FILES:
        file = request.FILES['file']
        fname = file.name
        fsize = file.size
        fp = open('%s%s' %(UPLOAD_DIR ,fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()    
        
    board = Board(writer=request.user,
                  title = request.POST['title'],
                  content=request.POST['content'],
                  filename=fname,
                  filesize=fsize)
    board.save()
    return redirect('/list/')

# list (Paginator 이용)
def list(request):
    page = request.GET.get('page',1)
    word = request.GET.get('word','')
    print('word : ', word)

    boardCount = Board.objects.filter(Q(title__contains=word)|
                                      Q(content__contains=word)|
                                      Q(writer__username__contains=word)).count() 
    boardList= Board.objects.filter(Q(title__contains=word)|
                                    Q(content__contains=word)|
                                    Q(writer__username__icontains=word)).order_by('-id')
                                    #icontains 대소문자 무시

    pageSize = 5
    # 페이징처리
    paginater = Paginator(boardList, pageSize) 
    page_obj = paginater.get_page(page)
    rowNo = boardCount-(int(page)-1)*pageSize 

    context = {'page_list' : page_obj,
               'page' : page,
               'word' : word,
               'rowNo': rowNo,
               'boardCount':boardCount  }
    return render(request, 'board/list.html', context)


def recommend_district_view(request):
    if request.method == 'POST':
        # 사용자가 입력한 데이터 가져오기
        price = int(request.POST['price'])
        hospital = int(request.POST['hospital'])
        bus = int(request.POST['bus'])
        convenience = int(request.POST['convenience'])
        subway = int(request.POST['subway'])
        department = int(request.POST['department'])
        office = int(request.POST['office'])
        mart = int(request.POST['mart'])
        kindergarten = int(request.POST['kindergarten'])
        library = int(request.POST['library'])
        park = int(request.POST['park'])
        school = int(request.POST['school'])
        bank = int(request.POST['bank'])
        senior = int(request.POST['senior'])

        # 사용자 입력을 리스트로 저장
        input_user = [price, hospital, bus, convenience, subway, department,
                      office, mart, kindergarten, library, park, school,
                      bank, senior]

        # recommend_district 함수 호출하여 추천 구 계산 후 변수에 저장
        recommended_gu = recommend_district(input_user)

        # 추천 결과를 HTML 템플릿에 전달
        return render(request, 'recommendation.html', {'recommended_gu': recommended_gu})

    # GET 요청일 경우, 빈 폼을 보여줌
    return render(request, 'recommendation.html')
