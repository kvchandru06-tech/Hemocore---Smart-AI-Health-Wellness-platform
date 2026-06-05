# medical_conditions.py
"""
Comprehensive medical conditions analyzer for blood reports
Analyzes 11+ conditions: Anemia, Infection, Leukopenia, Thrombocytopenia, 
Thrombocytosis, Dyslipidemia, Cardiac Risk, Kidney Dysfunction, 
Dehydration, Chronic Kidney Disease, Liver Damage
"""

def analyze_all_conditions(features):
    """
    Analyze blood report for multiple medical conditions
    Returns detailed analysis for each condition
    """
    conditions = {}
    
    # 1. ANEMIA ANALYSIS
    conditions['anemia'] = analyze_anemia(features)
    
    # 2. INFECTION/INFLAMMATION ANALYSIS
    conditions['infection'] = analyze_infection(features)
    
    # 3. LEUKOPENIA/LEUKOCYTOSIS
    conditions['leukocyte_disorders'] = analyze_leukocytes(features)
    
    # 4. PLATELET DISORDERS (Thrombocytopenia/Thrombocytosis)
    conditions['platelet_disorders'] = analyze_platelets(features)
    
    # 5. DYSLIPIDEMIA (Cholesterol/Lipids)
    conditions['dyslipidemia'] = analyze_lipids(features)
    
    # 6. CARDIAC RISK
    conditions['cardiac_risk'] = analyze_cardiac_risk(features)
    
    # 7. KIDNEY FUNCTION (Kidney Dysfunction/CKD)
    conditions['kidney_function'] = analyze_kidney_function(features)
    
    # 8. DEHYDRATION
    conditions['dehydration'] = analyze_dehydration(features)
    
    # 9. LIVER FUNCTION
    conditions['liver_function'] = analyze_liver_function(features)
    
    # 10. OVERALL HEALTH SCORE
    conditions['health_score'] = calculate_health_score(conditions)
    
    return conditions

def analyze_anemia(features):
    """Analyze for different types of anemia"""
    hb = features.get('Hemoglobin')
    rbc = features.get('RBC_COUNT')
    mcv = features.get('MCV')
    mch = features.get('MCH')
    mchc = features.get('MCHC')
    rdw = features.get('RDW')
    
    analysis = {
        'present': False,
        'severity': 'Normal',
        'type': None,
        'details': [],
        'recommendations': []
    }
    
    if hb:
        # Anemia severity based on hemoglobin
        if hb < 13:  # Anemia threshold (male) - for female it's <12
            analysis['present'] = True
            
            if hb >= 11: analysis['severity'] = 'Mild'
            elif hb >= 8: analysis['severity'] = 'Moderate'
            else: analysis['severity'] = 'Severe'
            
            analysis['details'].append(f"Hemoglobin: {hb} g/dL (Low)")
            
            # Determine anemia type
            if mcv:
                if mcv < 80:  # Microcytic
                    analysis['type'] = 'Microcytic Hypochromic Anemia'
                    analysis['details'].append(f"MCV: {mcv} fL (Low - microcytic)")
                    analysis['details'].append("Possible causes: Iron deficiency, thalassemia")
                    analysis['recommendations'].append("Iron supplements or increased dietary iron")
                    analysis['recommendations'].append("Consider iron studies and ferritin test")
                elif mcv > 100:  # Macrocytic
                    analysis['type'] = 'Macrocytic Anemia'
                    analysis['details'].append(f"MCV: {mcv} fL (High - macrocytic)")
                    analysis['details'].append("Possible causes: B12/Folate deficiency, hypothyroidism")
                    analysis['recommendations'].append("B12 and folate supplements")
                    analysis['recommendations'].append("Check thyroid function")
                else:  # Normocytic (80-100)
                    analysis['type'] = 'Normocytic Anemia'
                    analysis['details'].append(f"MCV: {mcv} fL (Normal)")
                    analysis['details'].append("Possible causes: Chronic disease, hemolysis, bone marrow issues")
                    analysis['recommendations'].append("Further investigation needed")
    
    if rbc and rbc < 4.5:
        analysis['details'].append(f"RBC Count: {rbc} mill/comm (Low)")
    
    return analysis

def analyze_infection(features):
    """Analyze for infection/inflammation"""
    wbc = features.get('WBC_COUNT')
    neutrophils = features.get('Neutrophils')
    lymphocytes = features.get('Lymphocytes')
    
    analysis = {
        'present': False,
        'type': None,
        'severity': 'Normal',
        'details': [],
        'recommendations': []
    }
    
    # Check WBC count
    if wbc:
        if wbc > 11000:  # Leukocytosis
            analysis['present'] = True
            analysis['type'] = 'Possible Infection/Inflammation'
            analysis['severity'] = 'Mild' if wbc < 15000 else 'Moderate' if wbc < 20000 else 'Severe'
            analysis['details'].append(f"WBC Count: {wbc} (High)")
            
            # Differential analysis
            if neutrophils and neutrophils > 70:
                analysis['type'] = 'Likely Bacterial Infection'
                analysis['details'].append(f"Neutrophils: {neutrophils}% (High - suggests bacterial)")
                analysis['recommendations'].append("Consider antibiotic treatment if symptomatic")
            elif lymphocytes and lymphocytes > 50:
                analysis['type'] = 'Possible Viral Infection'
                analysis['details'].append(f"Lymphocytes: {lymphocytes}% (High - suggests viral)")
                analysis['recommendations'].append("Antiviral treatment if indicated")
        
        elif wbc < 4000:  # Leukopenia
            analysis['present'] = True
            analysis['type'] = 'Leukopenia'
            analysis['severity'] = 'Mild' if wbc > 3000 else 'Moderate' if wbc > 2000 else 'Severe'
            analysis['details'].append(f"WBC Count: {wbc} (Low)")
            analysis['recommendations'].append("Investigate cause: viral infection, medication side effect, bone marrow issue")
            analysis['recommendations'].append("Consider repeat test and differential count")
    
    return analysis

def analyze_leukocytes(features):
    """Detailed leukocyte analysis (Leukopenia/Leukocytosis)"""
    wbc = features.get('WBC_COUNT')
    neutrophils = features.get('Neutrophils')
    lymphocytes = features.get('Lymphocytes')
    eosinophils = features.get('Eosinophils')
    monocytes = features.get('Monocytes')
    basophils = features.get('Basophils')
    
    analysis = {
        'total_wbc': wbc,
        'status': 'Normal',
        'abnormalities': [],
        'differential': {}
    }
    
    if wbc:
        if wbc > 11000:
            analysis['status'] = 'Leukocytosis (High WBC)'
            analysis['abnormalities'].append(f"Leukocytosis: WBC = {wbc} (Normal: 4000-11000)")
        elif wbc < 4000:
            analysis['status'] = 'Leukopenia (Low WBC)'
            analysis['abnormalities'].append(f"Leukopenia: WBC = {wbc} (Normal: 4000-11000)")
        else:
            analysis['status'] = 'Normal'
        
        analysis['differential']['total'] = f"{wbc} cells/cumm"
    
    # Analyze each type
    if neutrophils:
        if neutrophils > 70:
            analysis['abnormalities'].append(f"Neutrophilia ({neutrophils}%) - suggests bacterial infection, inflammation")
        elif neutrophils < 40:
            analysis['abnormalities'].append(f"Neutropenia ({neutrophils}%) - risk of infection")
        analysis['differential']['neutrophils'] = f"{neutrophils}%"
    
    if lymphocytes:
        if lymphocytes > 50:
            analysis['abnormalities'].append(f"Lymphocytosis ({lymphocytes}%) - suggests viral infection, lymphoma")
        elif lymphocytes < 20:
            analysis['abnormalities'].append(f"Lymphopenia ({lymphocytes}%) - immune deficiency")
        analysis['differential']['lymphocytes'] = f"{lymphocytes}%"
    
    if eosinophils and eosinophils > 6:
        analysis['abnormalities'].append(f"Eosinophilia ({eosinophils}%) - suggests allergies, parasites, autoimmune")
        analysis['differential']['eosinophils'] = f"{eosinophils}%"
    
    if monocytes and monocytes > 10:
        analysis['abnormalities'].append(f"Monocytosis ({monocytes}%) - suggests chronic infection, autoimmune")
        analysis['differential']['monocytes'] = f"{monocytes}%"
    
    if basophils and basophils > 2:
        analysis['abnormalities'].append(f"Basophilia ({basophils}%) - rare, may indicate myeloproliferative disorder")
        analysis['differential']['basophils'] = f"{basophils}%"
    
    return analysis

def analyze_platelets(features):
    """Analyze platelet disorders (Thrombocytopenia/Thrombocytosis)"""
    platelets = features.get('Platelet_Count')
    
    analysis = {
        'present': False,
        'disorders': [],
        'details': [],
        'recommendations': []
    }
    
    if platelets:
        # Thrombocytopenia (low platelets)
        if platelets < 150000:
            analysis['present'] = True
            severity = 'Mild' if platelets > 100000 else 'Moderate' if platelets > 50000 else 'Severe'
            analysis['disorders'].append(f"Thrombocytopenia ({severity})")
            analysis['details'].append(f"Platelet Count: {platelets:,} (Low)")
            
            if platelets < 50000:
                analysis['recommendations'].append("Risk of bleeding - avoid contact sports, NSAIDs")
                analysis['recommendations'].append("Investigate cause: immune thrombocytopenia, medications, bone marrow issues")
            elif platelets < 100000:
                analysis['recommendations'].append("Monitor, investigate cause if persistent")
        
        # Thrombocytosis (high platelets)
        elif platelets > 450000:
            analysis['present'] = True
            severity = 'Mild' if platelets < 600000 else 'Moderate' if platelets < 900000 else 'Severe'
            analysis['disorders'].append(f"Thrombocytosis ({severity})")
            analysis['details'].append(f"Platelet Count: {platelets:,} (High)")
            analysis['recommendations'].append("Risk of blood clots - stay hydrated, avoid smoking")
            analysis['recommendations'].append("Investigate cause: iron deficiency, inflammation, myeloproliferative disorders")
        
        else:
            analysis['details'].append(f"Platelet Count: {platelets:,} (Normal)")
    
    return analysis

def analyze_lipids(features):
    """Analyze cholesterol and lipid disorders (Dyslipidemia)"""
    ldl = features.get('LDL')
    hdl = features.get('HDL')
    triglycerides = features.get('Triglycerides')
    total_chol = features.get('Total_Cholesterol')
    
    analysis = {
        'present': False,
        'type': None,
        'risk_level': 'Low',
        'details': [],
        'recommendations': []
    }
    
    abnormalities = []
    
    # LDL Cholesterol
    if ldl:
        if ldl >= 190:
            analysis['present'] = True
            analysis['type'] = 'Severe Hypercholesterolemia'
            analysis['risk_level'] = 'Very High'
            abnormalities.append(f"LDL: {ldl} mg/dL (Very High)")
            analysis['recommendations'].append("High-intensity statin therapy needed")
        elif ldl >= 160:
            analysis['present'] = True
            analysis['type'] = 'High LDL Cholesterol'
            analysis['risk_level'] = 'High'
            abnormalities.append(f"LDL: {ldl} mg/dL (High)")
            analysis['recommendations'].append("Moderate-high intensity statin therapy")
        elif ldl >= 130:
            analysis['present'] = True
            analysis['type'] = 'Borderline High LDL'
            analysis['risk_level'] = 'Borderline'
            abnormalities.append(f"LDL: {ldl} mg/dL (Borderline High)")
            analysis['recommendations'].append("Lifestyle modifications: diet and exercise")
    
    # HDL Cholesterol
    if hdl:
        if hdl < 40:
            analysis['present'] = True
            if analysis['type']:
                analysis['type'] += ' with Low HDL'
            else:
                analysis['type'] = 'Low HDL Cholesterol'
            abnormalities.append(f"HDL: {hdl} mg/dL (Low)")
            analysis['recommendations'].append("Aerobic exercise, omega-3 fatty acids")
        elif hdl >= 60:
            abnormalities.append(f"HDL: {hdl} mg/dL (Excellent - protective)")
    
    # Triglycerides
    if triglycerides:
        if triglycerides >= 500:
            analysis['present'] = True
            analysis['type'] = 'Severe Hypertriglyceridemia'
            analysis['risk_level'] = 'Very High'
            abnormalities.append(f"Triglycerides: {triglycerides} mg/dL (Very High)")
            analysis['recommendations'].append("Risk of pancreatitis - fibrate therapy needed")
        elif triglycerides >= 200:
            analysis['present'] = True
            if analysis['type']:
                analysis['type'] += ' with High Triglycerides'
            else:
                analysis['type'] = 'Hypertriglyceridemia'
            abnormalities.append(f"Triglycerides: {triglycerides} mg/dL (High)")
            analysis['recommendations'].append("Reduce sugar, alcohol, refined carbs")
    
    # Total Cholesterol
    if total_chol:
        if total_chol >= 240:
            analysis['present'] = True
            abnormalities.append(f"Total Cholesterol: {total_chol} mg/dL (High)")
        elif total_chol >= 200:
            abnormalities.append(f"Total Cholesterol: {total_chol} mg/dL (Borderline High)")
    
    analysis['details'] = abnormalities
    
    if not analysis['recommendations'] and analysis['present']:
        analysis['recommendations'].append("Consult doctor for lipid management plan")
    
    return analysis

def analyze_cardiac_risk(features):
    """Calculate cardiac risk score"""
    # Using simplified risk assessment
    hb = features.get('Hemoglobin', 13.5)
    platelets = features.get('Platelet_Count', 250000)
    ldl = features.get('LDL', 100)
    hdl = features.get('HDL', 50)
    triglycerides = features.get('Triglycerides', 150)
    age_factor = 30  # Assuming average age
    
    analysis = {
        'risk_score': 0,
        'category': 'Low',
        'factors': [],
        'recommendations': []
    }
    
    # Calculate risk score (simplified 0-100 scale)
    risk_points = 0
    
    # Anemia as risk factor
    if hb and hb < 13:
        risk_points += 15
        analysis['factors'].append(f"Anemia (Hb: {hb})")
    
    # High platelet count (pro-thrombotic state)
    if platelets and platelets > 450000:
        risk_points += 10
        analysis['factors'].append(f"Thrombocytosis (Platelets: {platelets:,})")
    
    # Dyslipidemia factors
    if ldl and ldl > 130:
        risk_points += 20
        analysis['factors'].append(f"High LDL ({ldl})")
    
    if hdl and hdl < 40:
        risk_points += 15
        analysis['factors'].append(f"Low HDL ({hdl})")
    
    if triglycerides and triglycerides > 200:
        risk_points += 10
        analysis['factors'].append(f"High Triglycerides ({triglycerides})")
    
    # Age factor (simplified)
    risk_points += min(age_factor // 10, 5) * 5
    
    # Categorize risk
    analysis['risk_score'] = min(risk_points, 100)
    
    if analysis['risk_score'] >= 70:
        analysis['category'] = 'High Risk'
        analysis['recommendations'].append("Cardiology consultation recommended")
        analysis['recommendations'].append("Lifestyle modification essential")
        analysis['recommendations'].append("Consider stress test if symptomatic")
    elif analysis['risk_score'] >= 50:
        analysis['category'] = 'Moderate Risk'
        analysis['recommendations'].append("Regular cardiac monitoring")
        analysis['recommendations'].append("Improve diet and exercise")
        analysis['recommendations'].append("Manage other risk factors")
    elif analysis['risk_score'] >= 30:
        analysis['category'] = 'Low Risk'
        analysis['recommendations'].append("Maintain healthy lifestyle")
        analysis['recommendations'].append("Regular check-ups")
    else:
        analysis['category'] = 'Very Low Risk'
        analysis['recommendations'].append("Continue healthy habits")
    
    return analysis

def analyze_kidney_function(features):
    """Analyze kidney function indicators (Kidney Dysfunction/CKD)"""
    creatinine = features.get('Creatinine')
    bun = features.get('BUN')
    egfr = features.get('eGFR')
    uric_acid = features.get('Uric_Acid')
    
    analysis = {
        'present': False,
        'stage': None,
        'details': [],
        'recommendations': []
    }
    
    abnormalities = []
    
    if creatinine:
        if creatinine > 1.2:  # High creatinine (male)
            analysis['present'] = True
            if creatinine <= 1.9:
                analysis['stage'] = 'Mild Kidney Impairment'
                abnormalities.append(f"Creatinine: {creatinine} mg/dL (Mildly elevated)")
                analysis['recommendations'].append("Stay hydrated, avoid NSAIDs")
                analysis['recommendations'].append("Monitor kidney function")
            elif creatinine <= 3.5:
                analysis['stage'] = 'Moderate Kidney Impairment'
                abnormalities.append(f"Creatinine: {creatinine} mg/dL (Moderately elevated)")
                analysis['recommendations'].append("Nephrology consultation recommended")
                analysis['recommendations'].append("Monitor blood pressure")
            else:
                analysis['stage'] = 'Severe Kidney Impairment'
                abnormalities.append(f"Creatinine: {creatinine} mg/dL (Severely elevated)")
                analysis['recommendations'].append("Urgent nephrology referral needed")
                analysis['recommendations'].append("Dietary protein restriction may be needed")
        else:
            abnormalities.append(f"Creatinine: {creatinine} mg/dL (Normal)")
    
    if bun and bun > 20:
        analysis['present'] = True
        abnormalities.append(f"BUN: {bun} mg/dL (High)")
        analysis['recommendations'].append("Possible dehydration or kidney issue")
    
    # eGFR if available
    if egfr:
        if egfr < 60:
            analysis['present'] = True
            # CKD staging based on eGFR
            if egfr >= 45:
                analysis['stage'] = 'CKD Stage 3a (Mild-Moderate)'
            elif egfr >= 30:
                analysis['stage'] = 'CKD Stage 3b (Moderate)'
            elif egfr >= 15:
                analysis['stage'] = 'CKD Stage 4 (Severe)'
            else:
                analysis['stage'] = 'CKD Stage 5 (Kidney Failure)'
            
            abnormalities.append(f"eGFR: {egfr} mL/min (Low)")
            analysis['recommendations'].append(f"{analysis['stage']} - specialist consultation needed")
        else:
            abnormalities.append(f"eGFR: {egfr} mL/min (Normal)")
    
    if uric_acid and uric_acid > 7.0:
        abnormalities.append(f"Uric Acid: {uric_acid} mg/dL (High)")
        analysis['recommendations'].append("Limit purine-rich foods (red meat, seafood)")
        analysis['recommendations'].append("Stay well hydrated")
    
    analysis['details'] = abnormalities
    
    if not analysis['present']:
        analysis['details'].append("Kidney function appears normal based on available parameters")
    
    return analysis

def analyze_dehydration(features):
    """Analyze dehydration markers"""
    hb = features.get('Hemoglobin')
    pcv = features.get('PCV')
    sodium = features.get('Sodium')
    
    analysis = {
        'present': False,
        'severity': None,
        'details': [],
        'recommendations': []
    }
    
    if pcv:
        # High PCV/Hematocrit suggests hemoconcentration (dehydration)
        if pcv > 50:  # Normal range 40-50%
            analysis['present'] = True
            if pcv <= 55:
                analysis['severity'] = 'Mild Dehydration'
                analysis['details'].append(f"PCV: {pcv}% (High - suggests mild dehydration)")
            elif pcv <= 60:
                analysis['severity'] = 'Moderate Dehydration'
                analysis['details'].append(f"PCV: {pcv}% (High - suggests moderate dehydration)")
            else:
                analysis['severity'] = 'Severe Dehydration'
                analysis['details'].append(f"PCV: {pcv}% (Very High - suggests severe dehydration)")
            
            analysis['recommendations'].append("Increase fluid intake (2-3 liters daily)")
            analysis['recommendations'].append("Monitor urine color (should be pale yellow)")
        else:
            analysis['details'].append(f"PCV: {pcv}% (Normal)")
    
    if hb and hb > 17:  # High hemoglobin can also suggest dehydration
        analysis['present'] = True
        analysis['details'].append(f"Hemoglobin: {hb} g/dL (High - may indicate dehydration)")
    
    if sodium and sodium > 145:  # Hypernatremia suggests dehydration
        analysis['present'] = True
        analysis['details'].append(f"Sodium: {sodium} mEq/L (High - suggests dehydration)")
        analysis['recommendations'].append("Gradual rehydration under medical supervision if severe")
    
    if not analysis['present']:
        analysis['details'].append("Hydration status appears normal")
    
    return analysis

def analyze_liver_function(features):
    """Analyze liver function indicators (Liver Damage)"""
    alt = features.get('ALT')
    ast = features.get('AST')
    alp = features.get('ALP')
    bilirubin_total = features.get('Bilirubin_Total')
    bilirubin_direct = features.get('Bilirubin_Direct')
    total_protein = features.get('Total_Protein')
    albumin = features.get('Albumin')
    
    analysis = {
        'present': False,
        'pattern': None,
        'details': [],
        'recommendations': []
    }
    
    abnormalities = []
    
    if alt and alt > 40:  # Elevated ALT
        abnormalities.append(f"ALT: {alt} U/L (High)")
        analysis['present'] = True
    
    if ast and ast > 40:  # Elevated AST
        abnormalities.append(f"AST: {ast} U/L (High)")
        analysis['present'] = True
    
    if alp and alp > 130:  # Elevated ALP
        abnormalities.append(f"ALP: {alp} U/L (High)")
        analysis['present'] = True
    
    if bilirubin_total and bilirubin_total > 1.2:  # Elevated bilirubin
        abnormalities.append(f"Total Bilirubin: {bilirubin_total} mg/dL (High)")
        analysis['present'] = True
        
        if bilirubin_direct:
            if bilirubin_direct > 0.3:
                abnormalities.append(f"Direct Bilirubin: {bilirubin_direct} mg/dL (High - suggests obstructive jaundice)")
            else:
                abnormalities.append(f"Direct Bilirubin: {bilirubin_direct} mg/dL (Normal - suggests hemolytic jaundice)")
    
    if total_protein and total_protein < 6.0:
        abnormalities.append(f"Total Protein: {total_protein} g/dL (Low)")
        analysis['present'] = True
    
    if albumin and albumin < 3.5:
        abnormalities.append(f"Albumin: {albumin} g/dL (Low)")
        analysis['present'] = True
    
    if abnormalities:
        analysis['details'] = abnormalities
        
        # Pattern recognition
        if alt and ast:
            ratio = ast / alt if alt > 0 else 0
            if ratio > 2.0:
                analysis['pattern'] = 'Alcoholic Liver Disease pattern (AST:ALT > 2:1)'
                analysis['recommendations'].append("Assess alcohol intake - complete abstinence recommended")
            elif alt > ast:
                analysis['pattern'] = 'Hepatocellular pattern (ALT dominant)'
                analysis['recommendations'].append("Possible hepatitis - check viral markers")
            else:
                analysis['pattern'] = 'Mixed pattern'
        
        if alp and alt:
            if alp > alt * 2:
                analysis['pattern'] = 'Cholestatic pattern (ALP dominant)'
                analysis['recommendations'].append("Possible biliary obstruction - ultrasound recommended")
        
        analysis['recommendations'].append("Avoid alcohol and hepatotoxic medications")
        analysis['recommendations'].append("Follow up with liver function tests")
        analysis['recommendations'].append("Consider liver ultrasound if abnormalities persist")
    else:
        analysis['details'].append("Liver function tests appear normal")
    
    return analysis

def calculate_health_score(conditions):
    """Calculate overall health score based on all conditions"""
    score = 100  # Start with perfect score
    
    deductions = []
    
    # Deduct points for each condition
    if conditions['anemia']['present']:
        if conditions['anemia']['severity'] == 'Severe':
            score -= 25
            deductions.append("-25: Severe anemia")
        elif conditions['anemia']['severity'] == 'Moderate':
            score -= 15
            deductions.append("-15: Moderate anemia")
        else:
            score -= 8
            deductions.append("-8: Mild anemia")
    
    if conditions['infection']['present']:
        if conditions['infection']['severity'] == 'Severe':
            score -= 20
            deductions.append("-20: Severe infection")
        elif conditions['infection']['severity'] == 'Moderate':
            score -= 12
            deductions.append("-12: Moderate infection")
        else:
            score -= 8
            deductions.append("-8: Mild infection")
    
    if conditions['platelet_disorders']['present']:
        score -= 12
        deductions.append("-12: Platelet disorder")
    
    if conditions['dyslipidemia']['present']:
        if conditions['dyslipidemia']['risk_level'] == 'Very High':
            score -= 18
            deductions.append("-18: Severe dyslipidemia")
        else:
            score -= 10
            deductions.append("-10: Dyslipidemia")
    
    if conditions['cardiac_risk']['category'] == 'High Risk':
        score -= 20
        deductions.append("-20: High cardiac risk")
    elif conditions['cardiac_risk']['category'] == 'Moderate Risk':
        score -= 12
        deductions.append("-12: Moderate cardiac risk")
    
    if conditions['kidney_function']['present']:
        if 'Severe' in str(conditions['kidney_function'].get('stage', '')):
            score -= 25
            deductions.append("-25: Severe kidney impairment")
        elif 'Moderate' in str(conditions['kidney_function'].get('stage', '')):
            score -= 15
            deductions.append("-15: Moderate kidney impairment")
        else:
            score -= 8
            deductions.append("-8: Mild kidney impairment")
    
    if conditions['dehydration']['present']:
        if conditions['dehydration']['severity'] == 'Severe':
            score -= 10
            deductions.append("-10: Severe dehydration")
        else:
            score -= 5
            deductions.append("-5: Dehydration")
    
    if conditions['liver_function']['present']:
        score -= 12
        deductions.append("-12: Liver function abnormality")
    
    # Ensure score doesn't go below 0
    score = max(0, min(100, score))
    
    # Categorize score
    if score >= 90:
        category = "Excellent"
    elif score >= 75:
        category = "Good"
    elif score >= 60:
        category = "Fair"
    elif score >= 40:
        category = "Poor"
    else:
        category = "Critical"
    
    return {
        'score': score,
        'category': category,
        'deductions': deductions
    }

def get_comprehensive_report(features):
    """Generate a comprehensive medical report"""
    conditions = analyze_all_conditions(features)
    
    report = []
    report.append("=" * 70)
    report.append("COMPREHENSIVE MEDICAL ANALYSIS REPORT")
    report.append("=" * 70)
    report.append("Generated by: AI Blood Report Analyzer")
    report.append(f"Timestamp: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 1. Health Score Summary
    health_score = conditions['health_score']
    report.append(f"OVERALL HEALTH SCORE: {health_score['score']}/100")
    report.append(f"HEALTH CATEGORY: {health_score['category']}")
    report.append("")
    
    if health_score['deductions']:
        report.append("Key Factors Affecting Health Score:")
        for deduction in health_score['deductions']:
            report.append(f"  • {deduction}")
        report.append("")
    
    # 2. Condition-by-condition analysis
    report.append("DETAILED CONDITION ANALYSIS:")
    report.append("-" * 40)
    
    # Anemia
    anemia = conditions['anemia']
    report.append("\n1. ANEMIA ANALYSIS:")
    if anemia['present']:
        report.append(f"   Status: DETECTED ({anemia['severity']})")
        report.append(f"   Type: {anemia['type'] or 'Type unspecified'}")
        for detail in anemia['details']:
            report.append(f"   • {detail}")
        if anemia['recommendations']:
            report.append("   Recommendations:")
            for rec in anemia['recommendations']:
                report.append(f"     - {rec}")
    else:
        report.append("   Status: No anemia detected ✓")
    report.append("")
    
    # Infection
    infection = conditions['infection']
    report.append("2. INFECTION/INFLAMMATION ANALYSIS:")
    if infection['present']:
        report.append(f"   Status: DETECTED ({infection['severity']})")
        report.append(f"   Type: {infection['type']}")
        for detail in infection['details']:
            report.append(f"   • {detail}")
        if infection['recommendations']:
            report.append("   Recommendations:")
            for rec in infection['recommendations']:
                report.append(f"     - {rec}")
    else:
        report.append("   Status: No infection detected ✓")
    report.append("")
    
    # Leukocyte Disorders
    leuko = conditions['leukocyte_disorders']
    report.append("3. WHITE BLOOD CELL ANALYSIS:")
    if leuko['abnormalities']:
        report.append(f"   Status: ABNORMAL ({leuko['status']})")
        for abn in leuko['abnormalities']:
            report.append(f"   • {abn}")
    else:
        report.append("   Status: Normal ✓")
    report.append("")
    
    # Platelet Disorders
    platelets = conditions['platelet_disorders']
    report.append("4. PLATELET ANALYSIS:")
    if platelets['present']:
        report.append("   Status: ABNORMAL")
        for disorder in platelets['disorders']:
            report.append(f"   • {disorder}")
        for detail in platelets['details']:
            report.append(f"   • {detail}")
        if platelets['recommendations']:
            report.append("   Recommendations:")
            for rec in platelets['recommendations']:
                report.append(f"     - {rec}")
    else:
        report.append("   Status: Normal ✓")
    report.append("")
    
    # Dyslipidemia
    lipids = conditions['dyslipidemia']
    report.append("5. CHOLESTEROL & LIPID ANALYSIS:")
    if lipids['present']:
        report.append(f"   Status: DETECTED ({lipids['risk_level']} risk)")
        report.append(f"   Type: {lipids['type']}")
        for detail in lipids['details']:
            report.append(f"   • {detail}")
        if lipids['recommendations']:
            report.append("   Recommendations:")
            for rec in lipids['recommendations']:
                report.append(f"     - {rec}")
    else:
        report.append("   Status: Normal ✓")
    report.append("")
    
    # Cardiac Risk
    cardiac = conditions['cardiac_risk']
    report.append("6. CARDIAC RISK ASSESSMENT:")
    report.append(f"   Risk Category: {cardiac['category']}")
    report.append(f"   Risk Score: {cardiac['risk_score']}/100")
    if cardiac['factors']:
        report.append("   Risk Factors Identified:")
        for factor in cardiac['factors']:
            report.append(f"   • {factor}")
    if cardiac['recommendations']:
        report.append("   Recommendations:")
        for rec in cardiac['recommendations']:
            report.append(f"     - {rec}")
    report.append("")
    
    # Kidney Function
    kidney = conditions['kidney_function']
    report.append("7. KIDNEY FUNCTION ANALYSIS:")
    if kidney['present']:
        report.append(f"   Status: IMPAIRED")
        if kidney['stage']:
            report.append(f"   Stage: {kidney['stage']}")
        for detail in kidney['details']:
            report.append(f"   • {detail}")
        if kidney['recommendations']:
            report.append("   Recommendations:")
            for rec in kidney['recommendations']:
                report.append(f"     - {rec}")
    else:
        report.append("   Status: Normal ✓")
    report.append("")
    
    # Dehydration
    dehydration = conditions['dehydration']
    report.append("8. HYDRATION STATUS:")
    if dehydration['present']:
        report.append(f"   Status: DEHYDRATED ({dehydration['severity']})")
        for detail in dehydration['details']:
            report.append(f"   • {detail}")
        if dehydration['recommendations']:
            report.append("   Recommendations:")
            for rec in dehydration['recommendations']:
                report.append(f"     - {rec}")
    else:
        report.append("   Status: Normal hydration ✓")
    report.append("")
    
    # Liver Function
    liver = conditions['liver_function']
    report.append("9. LIVER FUNCTION ANALYSIS:")
    if liver['present']:
        report.append("   Status: ABNORMAL")
        if liver['pattern']:
            report.append(f"   Pattern: {liver['pattern']}")
        for detail in liver['details']:
            report.append(f"   • {detail}")
        if liver['recommendations']:
            report.append("   Recommendations:")
            for rec in liver['recommendations']:
                report.append(f"     - {rec}")
    else:
        report.append("   Status: Normal ✓")
    report.append("")
    
    # Summary
    report.append("=" * 70)
    report.append("SUMMARY:")
    report.append("-" * 40)
    
    total_conditions = 9
    abnormal_conditions = sum([
        1 if conditions['anemia']['present'] else 0,
        1 if conditions['infection']['present'] else 0,
        1 if conditions['platelet_disorders']['present'] else 0,
        1 if conditions['dyslipidemia']['present'] else 0,
        1 if conditions['kidney_function']['present'] else 0,
        1 if conditions['liver_function']['present'] else 0,
        1 if conditions['dehydration']['present'] else 0,
        1 if conditions['leukocyte_disorders']['abnormalities'] else 0,
        1 if conditions['cardiac_risk']['category'] in ['Moderate Risk', 'High Risk'] else 0
    ])
    
    report.append(f"Total Conditions Analyzed: {total_conditions}")
    report.append(f"Abnormal Conditions Found: {abnormal_conditions}")
    report.append(f"Normal Conditions: {total_conditions - abnormal_conditions}")
    report.append("")
    
    report.append("=" * 70)
    report.append("IMPORTANT DISCLAIMER:")
    report.append("-" * 40)
    report.append("This is an AI-powered analysis based on the blood report data.")
    report.append("It is NOT a substitute for professional medical advice,")
    report.append("diagnosis, or treatment. Always consult with a qualified")
    report.append("healthcare provider for any health concerns.")
    report.append("")
    report.append("Bring this report to your doctor for discussion.")
    report.append("=" * 70)
    
    return "\n".join(report)

# Test function
if __name__ == "__main__":
    # Test with sample data
    test_features = {
        'Hemoglobin': 12.5,
        'RBC_COUNT': 4.8,
        'PCV': 48.5,
        'MCV': 82,
        'WBC_COUNT': 8500,
        'Platelet_Count': 180000,
        'Neutrophils': 65,
        'Lymphocytes': 28,
        'Creatinine': 1.1,
        'LDL': 145,
        'HDL': 38,
        'Triglycerides': 180
    }
    
    print("Testing Medical Conditions Module...")
    conditions = analyze_all_conditions(test_features)
    print(f"Health Score: {conditions['health_score']['score']}/100")
    print(f"Anemia detected: {conditions['anemia']['present']}")
    print(f"Dyslipidemia detected: {conditions['dyslipidemia']['present']}")
    print("Test completed successfully!")