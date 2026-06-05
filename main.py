# main.py - COMPLETE VERSION WITH MEDICAL CONDITIONS
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os, json, numpy as np

# Import your modules
from nutrition import get_nutrition_recommendations
from exercise import get_exercise_plan
from visualization import create_value_plot
from pdf_export import export_report_to_pdf
from disease_prediction import predict_diseases
from doctor_recommendation import recommend_doctors
from wellness import get_wellness_guidance
from image_analysis import analyze_blood_image
from notification import get_health_alerts
from dashboard import get_dashboard_stats

# New imports for enhanced features
from medical_conditions import analyze_all_conditions, get_comprehensive_report
from pdf_utils import extract_text_from_any_pdf, parse_features_from_text, get_feature_descriptions, get_normal_ranges
from ml_predictor import predictor  # Make sure you created this file

app = FastAPI(title="AI Blood Report Analyzer with Medical Conditions Analysis")

# 🔐 SESSION MIDDLEWARE
app.add_middleware(SessionMiddleware, secret_key="super-secret-key-for-blood-analyzer")

# Create directories
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

USERS_FILE = "data/users.json"

# ---------------- AUTH UTILITIES ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- ROOT (LOGIN FIRST) ----------------
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse("/login", status_code=302)

# ---------------- LOGIN ----------------
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    users = load_users()
    if username in users and users[username]["password"] == password:
        request.session["user"] = username
        return RedirectResponse("/upload", status_code=302)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid username or password"
    })

# ---------------- SIGNUP ----------------
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    users = load_users()
    if username in users:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "User already exists"
        })

    users[username] = {"password": password}
    save_users(users)
    request.session["user"] = username
    return RedirectResponse("/upload", status_code=302)

# ---------------- LOGOUT ----------------
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

# ---------------- UPLOAD (PROTECTED) ----------------
@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("upload.html", {"request": request})

# ---------------- ANALYZE (PROTECTED) - UPDATED WITH MEDICAL CONDITIONS ----------------
@app.post("/analyze", response_class=HTMLResponse)
async def analyze_report(
    request: Request,
    file: UploadFile = File(...),
    query: str = Form("")
):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)

    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": "Only PDF files are allowed"
        })

    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # Extract text from PDF with OCR fallback
        poppler_path = None
        # Try to auto-detect poppler
        possible_paths = [
            r"C:\poppler\bin",
            r"C:\Program Files\poppler\bin",
            "/usr/bin",
            "/usr/local/bin"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                poppler_path = path
                break
        
        pdf_text = extract_text_from_any_pdf(temp_path, poppler_path)
        
        # Parse features from text
        features = parse_features_from_text(pdf_text)
        
        if not features:
            analysis = "⚠️ Could not extract blood test values from this PDF.\nPlease upload a clear, standard blood report PDF."
            nutrition, exercise, plot_img, error = [], [], None, analysis
            medical_analysis = None
            comprehensive_report = ""
            ml_result = {"risk_level": "Unknown", "confidence": 0.0, "message": "No data extracted"}
        else:
            # Get ML prediction
            ml_result = predictor.predict_risk(features)
            
            # Get comprehensive medical analysis
            medical_analysis = analyze_all_conditions(features)
            comprehensive_report = get_comprehensive_report(features)
            
            # Generate detailed analysis
            analysis = f"""🧬 COMPREHENSIVE MEDICAL ANALYSIS REPORT
────────────────────────────────────────

📊 OVERVIEW:
• Overall Health Score: {medical_analysis['health_score']['score']}/100 ({medical_analysis['health_score']['category']})
• AI Risk Assessment: {ml_result['risk_level']} ({ml_result['confidence']:.1f}% confidence)
• Parameters Extracted: {len(features)}

🔍 KEY FINDINGS:"""
            
            # Add key findings from medical analysis
            key_findings = []
            
            if medical_analysis['anemia']['present']:
                key_findings.append(f"• 🩸 Anemia: {medical_analysis['anemia']['severity']} - {medical_analysis['anemia']['type'] or 'Type unspecified'}")
            
            if medical_analysis['infection']['present']:
                key_findings.append(f"• 🦠 Infection/Inflammation: {medical_analysis['infection']['type']} ({medical_analysis['infection']['severity']})")
            
            if medical_analysis['platelet_disorders']['present']:
                disorders = ", ".join(medical_analysis['platelet_disorders']['disorders'])
                key_findings.append(f"• 🩸 Platelet Disorder: {disorders}")
            
            if medical_analysis['dyslipidemia']['present']:
                key_findings.append(f"• 🍔 Dyslipidemia: {medical_analysis['dyslipidemia']['type']}")
            
            if medical_analysis['cardiac_risk']['category'] != 'Very Low Risk':
                key_findings.append(f"• ❤️ Cardiac Risk: {medical_analysis['cardiac_risk']['category']} (Score: {medical_analysis['cardiac_risk']['risk_score']}/100)")
            
            if medical_analysis['kidney_function']['present']:
                key_findings.append(f"• 🫀 Kidney Function: {medical_analysis['kidney_function']['stage'] or 'Impaired'}")
            
            if medical_analysis['dehydration']['present']:
                key_findings.append(f"• 💧 Dehydration: {medical_analysis['dehydration']['severity']}")
            
            if medical_analysis['liver_function']['present']:
                key_findings.append(f"• 🍺 Liver Function: Abnormal ({medical_analysis['liver_function']['pattern'] or 'Pattern detected'})")
            
            # Add leukocyte abnormalities
            if medical_analysis['leukocyte_disorders']['abnormalities']:
                for abn in medical_analysis['leukocyte_disorders']['abnormalities'][:2]:  # Show first 2
                    key_findings.append(f"• ⚪ {abn}")
                if len(medical_analysis['leukocyte_disorders']['abnormalities']) > 2:
                    key_findings.append(f"• ... and {len(medical_analysis['leukocyte_disorders']['abnormalities']) - 2} more leukocyte abnormalities")
            
            if key_findings:
                analysis += "\n" + "\n".join(key_findings)
            else:
                analysis += "\n• ✅ No major abnormalities detected"
            
            analysis += f"""

📋 EXTRACTED PARAMETERS ({len(features)} total):
────────────────────────────────────────"""
            
            # Group parameters by category
            cbc_params = ['Hemoglobin', 'RBC_COUNT', 'PCV', 'MCV', 'MCH', 'MCHC', 'RDW', 'WBC_COUNT', 'Platelet_Count']
            diff_params = ['Neutrophils', 'Lymphocytes', 'Eosinophils', 'Monocytes', 'Basophils']
            liver_params = ['ALT', 'AST', 'ALP', 'Bilirubin_Total', 'Bilirubin_Direct', 'Bilirubin_Indirect']
            kidney_params = ['Creatinine', 'BUN', 'eGFR', 'Uric_Acid']
            lipid_params = ['Total_Cholesterol', 'LDL', 'HDL', 'Triglycerides', 'VLDL']
            other_params = ['Fasting_Blood_Sugar', 'PP_Blood_Sugar', 'HbA1c', 'TSH', 'T3', 'T4', 'Vitamin_D', 'Vitamin_B12']
            
            categories = {
                "Complete Blood Count (CBC)": cbc_params,
                "Differential Count": diff_params,
                "Liver Function": liver_params,
                "Kidney Function": kidney_params,
                "Lipid Profile": lipid_params,
                "Other Tests": other_params
            }
            
            for category, params in categories.items():
                category_params = {k: v for k, v in features.items() if k in params}
                if category_params:
                    analysis += f"\n\n{category}:"
                    for key, value in category_params.items():
                        analysis += f"\n  • {key}: {value}"
            
            analysis += f"""

💡 RECOMMENDATION:
{ml_result['message']}

📊 Full analysis available in the 'Medical Analysis' section.
👨‍⚕️ Doctor recommendations in 'Doctor Referral' section.
🥗 Personalized nutrition plan in 'Nutrition' section.
"""
            
            nutrition = get_nutrition_recommendations(features)
            exercise = get_exercise_plan(features)
            plot_img = create_value_plot(features)
            error = None
            
            # Store all results in app state for other pages
            request.app.state.ml_result = ml_result
            request.app.state.medical_analysis = medical_analysis
            request.app.state.comprehensive_report = comprehensive_report
            request.app.state.features = features
            request.app.state.feature_descriptions = get_feature_descriptions()
            request.app.state.normal_ranges = get_normal_ranges()
        
        # Store basic info
        request.app.state.file_name = file.filename
        request.app.state.query = query
        request.app.state.nutrition = nutrition
        request.app.state.exercise = exercise
        request.app.state.plot_img = plot_img
        request.app.state.analysis = analysis
        
    except Exception as e:
        error_msg = f"Error processing PDF: {str(e)}"
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": error_msg
        })
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "file_name": file.filename,
        "query": query,
        "analysis": analysis,
        "error": error if 'error' in locals() else None,
        "feature_count": len(features) if 'features' in locals() else 0
    })

# ---------------- MEDICAL ANALYSIS PAGE ----------------
@app.get("/medical_analysis", response_class=HTMLResponse)
async def medical_analysis_page(request: Request):
    """Show detailed medical conditions analysis"""
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)
    
    medical_analysis = getattr(request.app.state, "medical_analysis", None)
    features = getattr(request.app.state, "features", {})
    comprehensive_report = getattr(request.app.state, "comprehensive_report", "")
    
    if not medical_analysis or not features:
        return templates.TemplateResponse("medical_analysis.html", {
            "request": request,
            "error": "No medical analysis available. Please upload a blood report first.",
            "features": {},
            "medical_analysis": None,
            "report": "",
            "feature_descriptions": {},
            "normal_ranges": {}
        })
    
    return templates.TemplateResponse("medical_analysis.html", {
        "request": request,
        "medical_analysis": medical_analysis,
        "features": features,
        "report": comprehensive_report,
        "feature_descriptions": getattr(request.app.state, "feature_descriptions", {}),
        "normal_ranges": getattr(request.app.state, "normal_ranges", {})
    })

# ---------------- CONDITION DETAIL PAGES ----------------
@app.get("/condition/{condition_name}", response_class=HTMLResponse)
async def condition_detail_page(request: Request, condition_name: str):
    """Show detailed analysis for a specific condition"""
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)
    
    medical_analysis = getattr(request.app.state, "medical_analysis", None)
    features = getattr(request.app.state, "features", {})
    
    if not medical_analysis:
        return RedirectResponse("/medical_analysis", status_code=302)
    
    # Map condition names to analysis keys
    condition_map = {
        'anemia': ('anemia', '🩸 Anemia Analysis'),
        'infection': ('infection', '🦠 Infection Analysis'),
        'leukocytes': ('leukocyte_disorders', '⚪ White Blood Cell Analysis'),
        'platelets': ('platelet_disorders', '🩸 Platelet Disorders'),
        'cholesterol': ('dyslipidemia', '🍔 Cholesterol & Lipid Analysis'),
        'cardiac': ('cardiac_risk', '❤️ Cardiac Risk Assessment'),
        'kidney': ('kidney_function', '🫀 Kidney Function Analysis'),
        'dehydration': ('dehydration', '💧 Dehydration Analysis'),
        'liver': ('liver_function', '🍺 Liver Function Analysis')
    }
    
    condition_key, condition_title = condition_map.get(condition_name.lower(), (None, None))
    
    if not condition_key or condition_key not in medical_analysis:
        return templates.TemplateResponse("condition_detail.html", {
            "request": request,
            "error": f"Analysis for '{condition_name}' not available",
            "condition_data": None,
            "condition_title": "Condition Not Found"
        })
    
    condition_data = medical_analysis[condition_key]
    
    return templates.TemplateResponse("condition_detail.html", {
        "request": request,
        "condition_data": condition_data,
        "condition_title": condition_title,
        "condition_name": condition_name,
        "features": features,
        "error": None
    })

# ---------------- EXISTING PAGES (Updated to include medical analysis) ----------------
@app.get("/nutrition", response_class=HTMLResponse)
async def nutrition_page(request: Request):
    features = getattr(request.app.state, "features", {})
    medical_analysis = getattr(request.app.state, "medical_analysis", None)
    
    # Get base nutrition recommendations
    base_nutrition = get_nutrition_recommendations(features)
    
    # Add medical condition specific recommendations
    enhanced_nutrition = base_nutrition.copy()
    
    if medical_analysis:
        if medical_analysis['anemia']['present']:
            if medical_analysis['anemia']['type'] and 'Iron' in medical_analysis['anemia']['type']:
                enhanced_nutrition.append("Iron-rich foods: Red meat, spinach, lentils, fortified cereals")
            elif medical_analysis['anemia']['type'] and 'B12' in medical_analysis['anemia']['type']:
                enhanced_nutrition.append("B12-rich foods: Meat, eggs, dairy, fortified plant milk")
        
        if medical_analysis['dyslipidemia']['present']:
            enhanced_nutrition.append("Heart-healthy fats: Avocados, nuts, olive oil, fatty fish")
            enhanced_nutrition.append("Limit saturated fats: Reduce red meat, butter, full-fat dairy")
        
        if medical_analysis['kidney_function']['present']:
            enhanced_nutrition.append("Kidney-friendly: Limit protein if severe, control potassium")
    
    return templates.TemplateResponse("nutrition.html", {
        "request": request,
        "nutrition": enhanced_nutrition,
        "medical_analysis": medical_analysis
    })

@app.get("/exercise", response_class=HTMLResponse)
async def exercise_page(request: Request):
    features = getattr(request.app.state, "features", {})
    medical_analysis = getattr(request.app.state, "medical_analysis", None)
    
    base_exercise = get_exercise_plan(features)
    enhanced_exercise = base_exercise.copy()
    
    if medical_analysis:
        if medical_analysis['anemia']['present'] and medical_analysis['anemia']['severity'] == 'Severe':
            enhanced_exercise.append("⚠️ Avoid strenuous exercise until anemia improves")
        
        if medical_analysis['cardiac_risk']['category'] == 'High Risk':
            enhanced_exercise.append("Cardiac rehab: Start with light walking, monitor heart rate")
        
        if medical_analysis['dehydration']['present']:
            enhanced_exercise.append("💧 Hydrate well before, during, and after exercise")
    
    return templates.TemplateResponse("exercise.html", {
        "request": request,
        "exercise": enhanced_exercise,
        "medical_analysis": medical_analysis
    })

@app.get("/visualization", response_class=HTMLResponse)
async def visualization_page(request: Request):
    plot_img = getattr(request.app.state, "plot_img", "/static/barplot.png")
    features = getattr(request.app.state, "features", {})
    
    return templates.TemplateResponse("visualization.html", {
        "request": request,
        "plot_img": plot_img,
        "feature_count": len(features) if features else 0
    })

@app.get("/export_pdf", response_class=HTMLResponse)
async def export_pdf_page(request: Request):
    features = getattr(request.app.state, "features", {})
    file_name = getattr(request.app.state, "file_name", "report.pdf")
    comprehensive_report = getattr(request.app.state, "comprehensive_report", "")

    if not features:
        return templates.TemplateResponse("export.html", {
            "request": request,
            "export_pdf": None,
            "error": "No data to export"
        })

    try:
        # Create enhanced PDF with medical analysis
        pdf_filename = file_name.replace(".pdf", "_medical_analysis.pdf")
        pdf_output_path = f"outputs/{pdf_filename}"
        
        # Use your existing PDF export function
        export_report_to_pdf(features, pdf_output_path)
        
        # Option: You could create a separate medical analysis PDF
        medical_pdf_path = f"outputs/medical_{pdf_filename}"
        
        return templates.TemplateResponse("export.html", {
            "request": request,
            "export_pdf": f"/download/{pdf_filename}",
            "medical_pdf": f"/download/medical_{pdf_filename}" if os.path.exists(medical_pdf_path) else None,
            "error": None
        })
    except Exception as e:
        return templates.TemplateResponse("export.html", {
            "request": request,
            "export_pdf": None,
            "error": f"Error creating PDF: {str(e)}"
        })

@app.get("/download/{pdf_name}")
async def download_report(pdf_name: str):
    file_path = f"outputs/{pdf_name}"
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=pdf_name
        )
    return HTMLResponse("File not found", status_code=404)

@app.get("/disease", response_class=HTMLResponse)
async def disease_page(request: Request):
    features = getattr(request.app.state, "features", {})
    medical_analysis = getattr(request.app.state, "medical_analysis", {})
    
    # Use both old and new analysis
    old_diseases, old_scores = predict_diseases(features) if features else ([], [])
    
    # Enhanced with medical analysis
    enhanced_diseases = []
    enhanced_scores = []
    
    # Add from old system
    for disease, score in zip(old_diseases, old_scores):
        enhanced_diseases.append(disease)
        enhanced_scores.append(score)
    
    # Add from medical analysis
    if medical_analysis:
        if medical_analysis['anemia']['present']:
            enhanced_diseases.append(f"Anemia ({medical_analysis['anemia']['type'] or 'Unspecified'})")
            enhanced_scores.append("High" if medical_analysis['anemia']['severity'] in ['Moderate', 'Severe'] else "Moderate")
        
        if medical_analysis['infection']['present']:
            enhanced_diseases.append(f"{medical_analysis['infection']['type']}")
            enhanced_scores.append("High" if medical_analysis['infection']['severity'] in ['Moderate', 'Severe'] else "Moderate")
        
        if medical_analysis['platelet_disorders']['present']:
            for disorder in medical_analysis['platelet_disorders']['disorders']:
                enhanced_diseases.append(disorder)
                enhanced_scores.append("Moderate")
    
    if not enhanced_diseases:
        enhanced_diseases.append("No major diseases detected")
        enhanced_scores.append("Low")
    
    return templates.TemplateResponse("disease.html", {
        "request": request,
        "disease_scores": list(zip(enhanced_diseases, enhanced_scores)),
        "error": None,
        "medical_analysis": medical_analysis
    })

@app.get("/doctor", response_class=HTMLResponse)
async def doctor_page(request: Request):
    features = getattr(request.app.state, "features", {})
    medical_analysis = getattr(request.app.state, "medical_analysis", {})
    
    # Get base recommendations
    base_doctors = recommend_doctors(features) if features else []
    
    # Enhanced with medical analysis
    enhanced_doctors = base_doctors.copy()
    
    if medical_analysis:
        if medical_analysis['anemia']['present']:
            enhanced_doctors.append("Hematologist - For detailed anemia evaluation")
        
        if medical_analysis['cardiac_risk']['category'] == 'High Risk':
            enhanced_doctors.append("Cardiologist - For cardiac risk assessment")
        
        if medical_analysis['kidney_function']['present'] and medical_analysis['kidney_function']['stage']:
            enhanced_doctors.append("Nephrologist - For kidney function evaluation")
        
        if medical_analysis['liver_function']['present']:
            enhanced_doctors.append("Gastroenterologist/Hepatologist - For liver function evaluation")
        
        if medical_analysis['dyslipidemia']['present']:
            enhanced_doctors.append("Endocrinologist - For lipid management")
    
    # Remove duplicates
    enhanced_doctors = list(dict.fromkeys(enhanced_doctors))
    
    if not enhanced_doctors:
        enhanced_doctors.append("No specific specialist required based on report")
    
    return templates.TemplateResponse("doctor.html", {
        "request": request,
        "doctors": enhanced_doctors,
        "error": None,
        "medical_analysis": medical_analysis
    })

@app.get("/wellness", response_class=HTMLResponse)
async def wellness_page(request: Request):
    features = getattr(request.app.state, "features", {})
    medical_analysis = getattr(request.app.state, "medical_analysis", {})
    
    base_wellness = get_wellness_guidance(features)
    enhanced_wellness = base_wellness.copy()
    
    if medical_analysis:
        health_score = medical_analysis.get('health_score', {})
        if health_score.get('score', 100) < 60:
            enhanced_wellness.append("⚠️ Your health score indicates need for comprehensive lifestyle changes")
            enhanced_wellness.append("Consider regular health check-ups every 3-6 months")
        
        if medical_analysis.get('dehydration', {}).get('present'):
            enhanced_wellness.append("💧 Aim for 8-10 glasses of water daily, more if active")
        
        if medical_analysis.get('cardiac_risk', {}).get('category') == 'High Risk':
            enhanced_wellness.append("❤️ Monitor blood pressure regularly, reduce salt intake")
    
    return templates.TemplateResponse("wellness.html", {
        "request": request,
        "wellness": enhanced_wellness,
        "health_score": medical_analysis.get('health_score', {}) if medical_analysis else {},
        "medical_analysis": medical_analysis
    })

@app.post("/image_analysis", response_class=HTMLResponse)
async def image_analysis_page(request: Request, img: UploadFile = File(...)):
    result, img_url = analyze_blood_image(img)
    return templates.TemplateResponse("image_analysis.html", {
        "request": request,
        "result": result,
        "img_url": img_url
    })

@app.get("/notification", response_class=HTMLResponse)
async def notification_page(request: Request):
    features = getattr(request.app.state, "features", {})
    medical_analysis = getattr(request.app.state, "medical_analysis", {})
    
    base_alerts = get_health_alerts(features)
    enhanced_alerts = base_alerts.copy()
    
    if medical_analysis:
        # Add critical alerts from medical analysis
        if medical_analysis['anemia']['present'] and medical_analysis['anemia']['severity'] == 'Severe':
            enhanced_alerts.append("🚨 CRITICAL: Severe anemia detected - Urgent medical attention needed")
        
        if medical_analysis['platelet_disorders']['present']:
            for disorder in medical_analysis['platelet_disorders']['disorders']:
                if 'Severe' in disorder:
                    enhanced_alerts.append(f"🚨 CRITICAL: {disorder} - Risk of bleeding/clotting")
        
        if medical_analysis['cardiac_risk']['category'] == 'High Risk':
            enhanced_alerts.append("⚠️ HIGH RISK: Elevated cardiac risk - Cardiology consult recommended")
        
        if medical_analysis['kidney_function']['present'] and 'Severe' in str(medical_analysis['kidney_function'].get('stage', '')):
            enhanced_alerts.append("🚨 CRITICAL: Severe kidney impairment - Nephrology consult urgently needed")
    
    return templates.TemplateResponse("notification.html", {
        "request": request,
        "alerts": enhanced_alerts,
        "alert_count": len(enhanced_alerts),
        "medical_analysis": medical_analysis
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    features = getattr(request.app.state, "features", {})
    medical_analysis = getattr(request.app.state, "medical_analysis", {})
    ml_result = getattr(request.app.state, "ml_result", {})
    
    # Get basic stats
    stats = get_dashboard_stats(features) if features else []
    
    # Add medical analysis stats
    if medical_analysis:
        health_score = medical_analysis.get('health_score', {})
        stats.append({"name": "Health Score", "value": f"{health_score.get('score', 0)}/100"})
        stats.append({"name": "Health Category", "value": health_score.get('category', 'Unknown')})
        
        # Count conditions detected
        conditions_detected = 0
        for key in ['anemia', 'infection', 'platelet_disorders', 'dyslipidemia', 
                   'kidney_function', 'liver_function', 'dehydration']:
            if medical_analysis.get(key, {}).get('present'):
                conditions_detected += 1
        
        stats.append({"name": "Conditions Detected", "value": conditions_detected})
    
    if ml_result:
        stats.append({"name": "AI Risk Level", "value": ml_result.get('risk_level', 'Unknown')})
        stats.append({"name": "AI Confidence", "value": f"{ml_result.get('confidence', 0):.1f}%"})
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "feature_count": len(features) if features else 0,
        "medical_analysis": medical_analysis
    })

@app.get("/ml_results", response_class=HTMLResponse)
async def ml_results_page(request: Request):
    """Show ML analysis results"""
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)
    
    ml_result = getattr(request.app.state, "ml_result", None)
    features = getattr(request.app.state, "features", {})
    
    if not ml_result:
        return templates.TemplateResponse("ml_results.html", {
            "request": request,
            "error": "No ML analysis available. Please upload a report first.",
            "ml_result": None,
            "features": {}
        })
    
    return templates.TemplateResponse("ml_results.html", {
        "request": request,
        "ml_result": ml_result,
        "features": features,
        "error": None
    })

@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request):
    return templates.TemplateResponse("result.html", {
        "request": request,
        "file_name": getattr(request.app.state, "file_name", ""),
        "query": getattr(request.app.state, "query", ""),
        "analysis": getattr(request.app.state, "analysis", ""),
        "error": None,
        "feature_count": len(getattr(request.app.state, "features", {}))
    })

@app.get("/features", response_class=HTMLResponse)
async def features_page(request: Request):
    """Show all extracted features with descriptions"""
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)
    
    features = getattr(request.app.state, "features", {})
    descriptions = getattr(request.app.state, "feature_descriptions", {})
    normal_ranges = getattr(request.app.state, "normal_ranges", {})
    
    # Prepare feature data with descriptions and status
    feature_data = []
    for key, value in features.items():
        desc = descriptions.get(key, "No description available")
        
        # Check if value is within normal range
        status = "normal"
        if key in normal_ranges:
            range_info = normal_ranges[key]
            if isinstance(range_info, dict) and 'min' in range_info and 'max' in range_info:
                if value < range_info['min']:
                    status = "low"
                elif value > range_info['max']:
                    status = "high"
                else:
                    status = "normal"
        
        feature_data.append({
            "name": key,
            "value": value,
            "description": desc,
            "status": status,
            "unit": normal_ranges.get(key, {}).get('unit', ''),
            "normal_range": f"{normal_ranges.get(key, {}).get('min', '')} - {normal_ranges.get(key, {}).get('max', '')}" 
                          if isinstance(normal_ranges.get(key), dict) else ""
        })
    
    return templates.TemplateResponse("features.html", {
        "request": request,
        "features": feature_data,
        "total_features": len(feature_data)
    })

# ---------------- HEALTH HISTORY (Optional - Basic Implementation) ----------------
@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    """Show analysis history for the user"""
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)
    
    user = request.session["user"]
    history_file = f"data/{user}_history.json"
    
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except:
            history = []
    
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": history[-10:],  # Last 10 reports
        "username": user
    })

# ---------------- ABOUT/HELP PAGES ----------------
@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "conditions": [
            "Anemia", "Infection", "Leukopenia", "Thrombocytopenia",
            "Thrombocytosis", "Dyslipidemia", "Cardiac Risk",
            "Kidney Dysfunction", "Dehydration", "Chronic Kidney Disease",
            "Liver Damage"
        ]
    })

@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})

# ---------------- ERROR HANDLING ----------------
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error(request: Request, exc):
    return templates.TemplateResponse("500.html", {"request": request}, status_code=500)

# ---------------- STARTUP EVENT ----------------
@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🏥 AI Blood Report Analyzer with Medical Conditions")
    print("=" * 60)
    print("✅ Server starting...")
    print(f"✅ Data directory: {os.path.abspath('data')}")
    print(f"✅ Outputs directory: {os.path.abspath('outputs')}")
    print(f"✅ Static files: {os.path.abspath('static')}")
    print("✅ Medical conditions module loaded")
    print("✅ ML predictor initialized")
    print("=" * 60)
    print("📌 Available at: http://localhost:8000")
    print("📌 Login with: chandru or 2306")
    print("=" * 60)

# Run with: uvicorn main:app --reload --port 8000