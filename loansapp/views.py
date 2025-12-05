from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from . import mock_data   # import the clients data
def index(request):
    return render(request, 'index.html')


def clients(request):
    # Pass mock data into the template for viewing
    context = {
        "salary_data": mock_data.salary_data,
        "credit_data": mock_data.credit_data,
    }
    return render(request, 'clients.html', context)

@csrf_exempt
@csrf_exempt
def loan_eligibility(request):
    if request.method == "POST":
        data = json.loads(request.body)

        national_id = data.get("national_id")
        loan_amount = float(data.get("loan_amount"))
        term_months = int(data.get("term_months"))

        monthly_repayment = loan_amount / term_months

        # Salary Verification
        try:
            salary_resp = requests.get(f"http://localhost:8000/api/salary/{national_id}")
            salary_data = salary_resp.json()
            if "error" in salary_data:
                return JsonResponse({"eligible": False, "reasons": ["Applicant not found in salary records"]})
            monthly_salary = salary_data.get("monthly_salary", 0)
        except Exception:
            return JsonResponse({"status": "error", "reason": "Salary API unavailable"}, status=500)

        # Credit Bureau
        try:
            credit_resp = requests.get(f"http://localhost:8000/api/credit/{national_id}")
            credit_data = credit_resp.json()
            if "error" in credit_data:
                return JsonResponse({"eligible": False, "reasons": ["Applicant not found in credit bureau"]})
            credit_score = credit_data.get("credit_score", 0)
            active_defaults = credit_data.get("active_defaults", 0)
            active_loans = credit_data.get("active_loans", 0)
        except Exception:
            return JsonResponse({"status": "error", "reason": "Credit Bureau API unavailable"}, status=500)

        # Eligibility Rules
        reasons = []
        if monthly_salary < 3 * monthly_repayment:
            reasons.append("Salary too low for monthly repayment")
        if credit_score < 600:
            reasons.append("Credit score below 600")
        if active_defaults > 0:
            reasons.append("Active defaults present")
        if active_loans > 3:
            reasons.append("Too many active loans")

        if reasons:
            return JsonResponse({"eligible": False, "reasons": reasons})
        else:
            return JsonResponse({"eligible": True, "message": "Loan approved"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def credit_bureau(request, national_id):
    mock_data = {
        "12345": {"credit_score": 700, "active_defaults": 0, "active_loans": 2},
        "67890": {"credit_score": 550, "active_defaults": 1, "active_loans": 4},
    }
    if national_id in mock_data:
        return JsonResponse(mock_data[national_id])
    else:
        return JsonResponse({"error": "ID not found in credit bureau"}, status=404)

def salary_verification(request, national_id):
    mock_data = {
        "12345": {"monthly_salary": 1500},
        "67890": {"monthly_salary": 400},
    }
    if national_id in mock_data:
        return JsonResponse(mock_data[national_id])
    else:
        return JsonResponse({"error": "ID not found in salary records"}, status=404)
