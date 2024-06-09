from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
from datetime import date
from authapp.models import *
from quiz.models import *

@login_required(redirect_field_name='', login_url='/login/')
def evaluation(request):
    user=request.user
    try:
        info= profiledb.objects.get(user=user)
        status= "valid"
    except ObjectDoesNotExist:
        status= "invalid"
    return render (request, 'quiz/evaluation.html', {'status':status})
    
@login_required(redirect_field_name='', login_url='/login/')
def quizlist(request):
    return render(request, 'quizlist.html')
     

@login_required(redirect_field_name='', login_url='/login/')
def quizresult(request):
    if request.method =="POST":
        dimension= int(request.POST['dimension'])
        if (dimension == 13):
            results= wellnessCircle.objects.filter(user=request.user).order_by('-date')
            if (results):
                return render(request, 'quizresult.html',{'results'      : results,
                                                          'dimensionName': 'نتیجه تمامی ابعاد' })
            else:
                return render(request, 'quizresult.html',{'dimensionName': 'نتیجه تمامی ابعاد',
                                                          'message'      : 'نتیجه‌ای برای نمایش وجود ندارد.' })
        else:
            dimensionNames= ["مسئولیت پذیری در قبال خود و عشق", "تنفس","تغذیه","حس کردن","حرکت", "احساس کردن", "فکر کردن", "بازی کردن و کار کردن", "ارتباط برقرار کردن", "صمیمیت", "یافتن معنا", "ورا رفتن"]
            results= submit.objects.filter(user=request.user, number=dimension).order_by('-date')
            if (results.count() > 0):
                 return render(request, 'quizresult.html',{'results'      : results,
                                                           'dimensionName': dimensionNames[dimension-1] })
            else:
                 return render(request, 'quizresult.html',{'dimensionName': dimensionNames[dimension-1],
                                                           'message'      : 'نتیجه‌ای برای نمایش وجود ندارد.' })
    else:
        return render(request, 'quizresultlist.html')
    
@login_required(redirect_field_name='', login_url='/login/')
def quiz(request,quiz_number):
    if request.method =="POST":
        n=int(request.path.split('/')[-1])
        scores=[]
        for i in range(10):
            scores.append(int(request.POST.get('q'+str(i))))
        submit.objects.create(user=request.user,number=str(n),response=json.dumps(scores))
        print("####################################################################")
        mydata=wellnessCircle.objects.filter(user=request.user)
        
        if len(mydata)==0:
            totalquiz=[0,0,0,0,0,0,0,0,0,0,0,0]
            totalquiz[n-1]=sum(scores)
            
            wellnessCircle.objects.create(user=request.user,totalquiz=totalquiz)
        else:
            temp=json.loads(mydata[0].totalquiz)
            temp[n-1]=sum(scores)
            mydata[0].totalquiz=json.dumps(temp)
            mydata[0].save()
        return HttpResponse(status=204)
    return render(request, 'quiz.html')

def article(request,quiz_number,question_number):
    return render(request,'quiz_doc/'+str(quiz_number)+'_'+str(question_number)+'.html')

@login_required(redirect_field_name='', login_url='/login/')    
def QuizIntroduction(request,quiz_number):
    today = date.today()
    if submit.objects.filter(user=request.user, number=quiz_number).exists():
        lastQuiz= submit.objects.filter(user=request.user, number=quiz_number).order_by('-date')[0]
        DateOflastQuiz = date(lastQuiz.date.year, lastQuiz.date.month, lastQuiz.date.day)
        difference = abs(DateOflastQuiz - today)
        if (difference.days < 45):
            D= 45 - difference.days
            return render(request, 'QuizIntroduction/'+str(quiz_number)+'.html' , {'status': 'invalid',
                                                                                    'RD'    : D      })
        else:
            if (lastQuiz.result == ""):
                return render(request, 'QuizIntroduction/'+str(quiz_number)+'.html' , {'status': 'WithoutResult'})
            else:
                return render(request, 'QuizIntroduction/'+str(quiz_number)+'.html' , {'status': 'valid',
                                                                                        'number': quiz_number})
    else:
        return render(request, 'QuizIntroduction/'+str(quiz_number)+'.html' , {'status': 'valid',
                                                                                'number': str(quiz_number) })