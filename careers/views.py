from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Career,Application
from .serializers import CareerSerializer,ApplicationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .find_resume_score import calculate_score
from django.shortcuts import render
from .find_resume_score import extract_text
import google.generativeai as genai
# genai.configure(api_key="AIzaSyD0EFExVF1KUbF2BIjPV6CArpDhaLxDpig")
genai.configure(api_key="AIzaSyDiwv7KCFVQnYWen7z0iRuPiXRlzWCNKqg")

class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

class ApplicationAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        data = request.data
        data["user"] = request.user.id
        
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Application successfully applied'})      
        return Response({'msg':'An Error Occured'},status=status.HTTP_400_BAD_REQUEST)
    

def admin_view(request):
    careers = Career.objects.all()  
    career_names = [career.title for career in careers]  
    return render(request, "index.html", {'career_names': career_names}) 


from django.shortcuts import render
from .forms import UploadForm

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def upload_files(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            job_description_file = request.FILES['job_description']
            resume_file = request.FILES['resume']
            job_description_file_text = extract_text(job_description_file)
            resume_file_text = extract_text(resume_file)
            input_prompt_template = """
                Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider that the job market is very competitive, and you should provide the best assistance for improving the resumes. Assign the percentage matching based on JD and the missing keywords with high accuracy.
                resume: {text}
                description: {jd}

                I want the response in one single string having the structure
                {{"JD_Match":1 - 100,"MissingKeywords":["Keyword1","Keyword2"],"Profile_Summary":""}}
            """
            
            percentage_query = """
                Hey, act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider that the job market is very competitive, and you should provide the best assistance for improving the resumes. Assign the percentage matching based on JD and the missing keywords with high accuracy.
                resume: {text}
                description: {jd}

                I want the response in one single string having the structure
                {{"gdp_score":1 - 100,"standard_test_score":1 - 100,"certification_score":1 - 100,"language_proficiency_score":1 - 100,"performance_matrics":"best/good/etc"}}
            """
            
            input_prompt = input_prompt_template.format(text=resume_file_text, jd=job_description_file_text)
            input_prompt2 = percentage_query.format(text=resume_file_text, jd=job_description_file_text)
            response = get_gemini_response(input_prompt)
            response2 = get_gemini_response(input_prompt2)
            response_json = eval(response)
            response_json2 = eval(response2)
            # print(response_json)
            print(response_json2)
            return render(request, 'success.html', {'data': response_json,'data2':response_json2})
    else:
        form = UploadForm()
    return render(request, 'file_upload.html', {'form': form})
