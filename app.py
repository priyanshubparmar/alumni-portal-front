import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Alumni Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit as st
import requests

API_URL = "https://alumni-backend-1myt.onrender.com"
# API_URL1 = "https://alumni-backend-1myt.onrender.com/docs"
# try:
#     response = requests.get(API_URL1)
#     response.raise_for_status()  # Raises an HTTPError for bad responses
#     alumni_data = response.json()
#     st.write(alumni_data)
# except requests.exceptions.RequestException as e:
#     st.error(f"⚠️ Could not fetch alumni data from server.")

# =================== SESSION STATE ===================
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Home"
if "selected_alumni" not in st.session_state:
    st.session_state["selected_alumni"] = None
if "page_number" not in st.session_state:
    st.session_state["page_number"] = 1

# =================== NAVIGATION SETUP ===================
PAGES = [
    "🏠 Home",
    "👥 View Alumni + 🔍 Sort/Search", 
    "✍️ Create Alumni & Upload Photo",
    "🔧 Manage Alumni (Update/Delete)"
]

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
current_page = st.sidebar.radio("Choose Page:", PAGES)
st.session_state["current_page"] = current_page

# =================== HELPER FUNCTIONS ===================
def render_alumni_card(d):
    """Enhanced alumni card with better styling"""
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        
        # Profile Photo
        with col1:
            if d.get("profile_photo"):
                try:
                    photo_url = f"{API_URL}/view_photo/{d['id']}"
                    st.image(photo_url, width=120, caption="📸")
                except:
                    st.image("https://via.placeholder.com/120x120/e0e0e0/808080?text=No+Photo", width=120)
            else:
                st.image("https://via.placeholder.com/120x120/e0e0e0/808080?text=No+Photo", width=120)
        
        # Alumni Info
        with col2:
            name = f"{d.get('firstname', '')} {d.get('surname', '')}".strip()
            st.subheader(f"👤 {name}")
            st.write(f"🆔 **ID:** {d.get('id', 'N/A')}")
            st.write(f"🎓 **Batch:** {d.get('batch', 'N/A')}")
            st.write(f"💼 **Position:** {d.get('current_position', 'N/A')}")
            st.write(f"🏢 **Organization:** {d.get('current_organization', 'N/A')}")
            st.write(f"🧑‍💼 **Experience:** {d.get('Industry_experiences', 0)} years")
            
            if d.get("linkedin_url"):
                st.markdown(f"🔗 [LinkedIn Profile]({d['linkedin_url']})")
        
        # Action Button
        with col3:
            if st.button(f"ℹ️ Details", key=f"detail_{d['id']}", help="View full details"):
                st.session_state["selected_alumni"] = d['id']
                st.rerun()

def render_alumni_details(d):
    """Detailed alumni view"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if d.get("profile_photo"):
            try:
                photo_url = f"{API_URL}/view_photo/{d['id']}"
                st.image(photo_url, width=250, caption=f"{d.get('firstname', '')} {d.get('surname', '')}")
            except:
                st.info("🖼️ No profile photo available")
        else:
            st.info("🖼️ No profile photo available")
    
    with col2:
        name = f"{d.get('firstname', '')} {d.get('surname', '')}".strip()
        st.header(f"👤 {name}")
        
        # Basic Info
        st.subheader("📋 Basic Information")
        st.write(f"🆔 **Alumni ID:** {d.get('id', 'N/A')}")
        st.write(f"🎓 **Batch:** {d.get('batch', 'N/A')}")
        st.write(f"⚧ **Gender:** {d.get('gender', 'N/A')}")
        
        # Professional Info
        st.subheader("💼 Professional Information")
        st.write(f"🏢 **Current Organization:** {d.get('current_organization', 'N/A')}")
        st.write(f"💼 **Current Position:** {d.get('current_position', 'N/A')}")
        st.write(f"📍 **Location:** {d.get('current_location', 'N/A')}")
        if d.get("Industry_experiences") is not None:
            st.write(f"🧑‍💼 **Experience:** {d['Industry_experiences']} years")
        
        if d.get("linkedin_url"):
            st.write(f"🔗 **LinkedIn:** [View Profile]({d['linkedin_url']})")
    
    # Skills sections
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🛠️ Software Skills")
        skills = []
        for i in range(1, 4):
            skill = d.get(f"software_skill_{i}")
            if skill and skill.strip():
                skills.append(f"• {skill}")
        
        if skills:
            for skill in skills:
                st.write(skill)
        else:
            st.write("*No software skills listed*")
    
    with col4:
        st.subheader("💻 Programming Languages")
        languages = []
        for i in range(1, 4):
            lang = d.get(f"programming_lang_{i}")
            if lang and lang.strip():
                languages.append(f"• {lang}")
        
        if languages:
            for lang in languages:
                st.write(lang)
        else:
            st.write("*No programming languages listed*")

# =================== MAIN TITLE ===================
st.title("🎓 Department of Statistics - Alumni Portal")
st.markdown("---")

# =================== PAGE 0: HOME ===================
if current_page == "🏠 Home":
    st.header("🏠 Welcome to the Alumni Portal")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📊 About This Portal
        This portal is an effort by the **Department of Statistics** to collect and showcase 
        information about alumni of the department from **Sardar Patel University**.
        
        ### 🎯 Features
        - **📝 Add Alumni:** Create new alumni profiles with photos
        - **👥 View Alumni:** Browse all alumni with search and filtering
        - **🔍 Advanced Search:** Sort by experience, filter by batch/gender
        - **🔧 Manage:** Update, delete, and modify alumni records
        
        ### 🚀 Get Started
        Use the navigation menu on the left to explore different sections of the portal.
        """)
    
    with col2:
        st.info("📌 **Developed by:**\n\n**Priyanshu B. Parmar**\n\n**Mail: parmarpriyanshubharat@gmail.com**\n\n 🎓 Applied Statistics Student, 📅 Batch 2024–26")
        
        # Quick stats
        try:
            response = requests.get(f"{API_URL}/view")
            if response.status_code == 200:
                data = response.json()
                total_alumni = len(data.get("alumni", {}))
                st.metric("📊 Total Alumni", total_alumni)
        except:
            st.metric("📊 Total Alumni", "N/A")

# =================== PAGE 1: VIEW ALUMNI ===================
elif current_page == "👥 View Alumni + 🔍 Sort/Search":
    st.header("👥 Alumni Records")
    
    try:
        response = requests.get(f"{API_URL}/view")
        if response.status_code == 200:
            data = response.json()
            alumni_records = data.get("alumni", {})
            
            if not alumni_records:
                st.info("📭 No alumni records found yet. Add some alumni first!")
            else:
                # Filters and Search
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    search_id = st.text_input("🔍 Search by Alumni ID", placeholder="e.g., 001-2008-09")
                
                with col2:
                    batches = sorted({d.get("batch") for d in alumni_records.values() if d.get("batch")})
                    batch_choice = st.selectbox("🎓 Filter by Batch", ["All Batches"] + batches)
                
                with col3:
                    genders = sorted({d.get("gender") for d in alumni_records.values() if d.get("gender")})
                    gender_choice = st.selectbox("⚧ Filter by Gender", ["All Genders"] + genders)
                
                with col4:
                    sort_options = ["None", "Experience ⬆️", "Experience ⬇️", "Name A-Z", "Name Z-A"]
                    sort_choice = st.selectbox("📊 Sort by", sort_options)
                
                # Apply filters
                filtered = {}
                for aid, d in alumni_records.items():
                    # Search filter
                    if search_id and search_id.lower() not in aid.lower():
                        continue
                    
                    # Batch filter
                    if batch_choice != "All Batches" and d.get("batch") != batch_choice:
                        continue
                    
                    # Gender filter
                    if gender_choice != "All Genders" and d.get("gender") != gender_choice:
                        continue
                    
                    filtered[aid] = d
                
                # Apply sorting
                if sort_choice == "Experience ⬆️":
                    filtered = dict(sorted(filtered.items(), 
                                         key=lambda kv: kv[1].get("Industry_experiences", 0)))
                elif sort_choice == "Experience ⬇️":
                    filtered = dict(sorted(filtered.items(), 
                                         key=lambda kv: kv[1].get("Industry_experiences", 0), reverse=True))
                elif sort_choice == "Name A-Z":
                    filtered = dict(sorted(filtered.items(), 
                                         key=lambda kv: f"{kv[1].get('firstname', '')} {kv[1].get('surname', '')}"))
                elif sort_choice == "Name Z-A":
                    filtered = dict(sorted(filtered.items(), 
                                         key=lambda kv: f"{kv[1].get('firstname', '')} {kv[1].get('surname', '')}", reverse=True))
                
                # Pagination
                st.markdown("---")
                total_records = len(filtered)
                records_per_page = 5
                total_pages = max(1, (total_records - 1) // records_per_page + 1)
                
                if total_records > 0:
                    col_prev, col_page, col_next = st.columns([1, 2, 1])
                    
                    with col_prev:
                        if st.button("⬅️ Previous", disabled=(st.session_state["page_number"] <= 1)):
                            st.session_state["page_number"] -= 1
                            st.rerun()
                    
                    with col_page:
                        st.write(f"📄 Page {st.session_state['page_number']} of {total_pages} | 📊 {total_records} alumni found")
                    
                    with col_next:
                        if st.button("➡️ Next", disabled=(st.session_state["page_number"] >= total_pages)):
                            st.session_state["page_number"] += 1
                            st.rerun()
                    
                    # Show records for current page
                    start_idx = (st.session_state["page_number"] - 1) * records_per_page
                    end_idx = start_idx + records_per_page
                    current_records = list(filtered.items())[start_idx:end_idx]
                    
                    for aid, d in current_records:
                        render_alumni_card(d)
                        
                        # Expandable details
                        with st.expander(f"📋 Full Details for {d.get('firstname', '')} {d.get('surname', '')}"):
                            render_alumni_details(d)
                        
                        st.markdown("---")
                else:
                    st.warning("🔍 No alumni found matching your criteria.")
        
        else:
            st.error("⚠️ Could not fetch alumni data from server.")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# =================== PAGE 2: CREATE ALUMNI ===================
elif current_page == "✍️ Create Alumni & Upload Photo":
    st.header("➕ Create New Alumni Profile")
    
    with st.form("alumni_form", clear_on_submit=False):
        st.subheader("📋 Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            firstname = st.text_input("First Name *", help="Required field")
            surname = st.text_input("Surname", help="Optional")
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            batch = st.text_input("Batch (e.g., 2008-09) *", help="Format: YYYY-YY")
        
        with col2:
            linkedin_url = st.text_input("LinkedIn URL *", help="Full LinkedIn profile URL")
            current_organization = st.text_input("Current Organization")
            current_position = st.text_input("Current Position")
            current_location = st.text_input("Current Location")
        
        st.subheader("💼 Professional Details")
        experience = st.number_input("Years of Industry Experience", 
                                   min_value=0.0, max_value=50.0, step=0.5, value=0.0)
        
        st.subheader("🛠️ Technical Skills")
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("**Software Skills**")
            software_skill_1 = st.text_input("Software Skill 1", placeholder="e.g., SPSS")
            software_skill_2 = st.text_input("Software Skill 2", placeholder="e.g., R Studio")
            software_skill_3 = st.text_input("Software Skill 3", placeholder="e.g., Excel")
        
        with col4:
            st.write("**Programming Languages**")
            programming_lang_1 = st.text_input("Programming Language 1", placeholder="e.g., Python")
            programming_lang_2 = st.text_input("Programming Language 2", placeholder="e.g., R")
            programming_lang_3 = st.text_input("Programming Language 3", placeholder="e.g., SQL")
        
        st.subheader("📸 Profile Photo")
        photo = st.file_uploader("Upload Profile Photo (size should be Less Then 5MB)", 
                                type=["jpg", "jpeg", "png"], 
                                help="Supported formats: JPG, JPEG, PNG")
        
        st.markdown("---")
        submitted = st.form_submit_button("🚀 Submit Alumni Data", use_container_width=True)
    
    if submitted:
        # Validate required fields
        if not firstname or not gender or not batch or not linkedin_url:
            st.error("⚠️ Please fill in all required fields marked with *")
        else:
            alumni_data = {
                "id": "temp",  # Backend will generate this
                "firstname": firstname,
                "surname": surname or None,
                "gender": gender,
                "batch": batch,
                "linkedin_url": linkedin_url,
                "current_organization": current_organization or None,
                "current_position": current_position or None,
                "current_location": current_location or None,
                "Industry_experiences": experience,
                "software_skill_1": software_skill_1 or None,
                "software_skill_2": software_skill_2 or None,
                "software_skill_3": software_skill_3 or None,
                "programming_lang_1": programming_lang_1 or None,
                "programming_lang_2": programming_lang_2 or None,
                "programming_lang_3": programming_lang_3 or None,
                "profile_photo": None,
            }
            
            try:
                with st.spinner("Creating alumni record..."):
                    resp = requests.post(f"{API_URL}/create_alumni", json=alumni_data)
                
                if resp.status_code in (200, 201):
                    result = resp.json()
                    alumni_id = result['id']
                    st.success(f"✅ Alumni created successfully! ID: **{alumni_id}**")
                    
                    if photo is not None:
                        with st.spinner("Uploading profile photo..."):
                            files = {
                                "profile_photo": (photo.name, photo.getvalue(), photo.type or "application/octet-stream")
                            }
                            upload_resp = requests.post(f"{API_URL}/upload_photo/{alumni_id}", files=files)
                            
                            if upload_resp.status_code == 200:
                                st.success("📸 Profile photo uploaded successfully!")
                            else:
                                st.warning("⚠️ Alumni created but photo upload failed. You can upload the photo later.")
                    
                    st.balloons()
                    
                    # Show created alumni info
                    st.subheader("📋 Created Alumni Summary")
                    st.write(f"**Name:** {firstname} {surname or ''}")
                    st.write(f"**ID:** {alumni_id}")
                    st.write(f"**Batch:** {batch}")
                    
                else:
                    error_detail = resp.text
                    st.error(f"❌ Failed to create alumni: {error_detail}")
                    
            except Exception as e:
                st.error(f"❌ Error occurred: {str(e)}")

# =================== PAGE 3: MANAGE ALUMNI ===================
elif current_page == "🔧 Manage Alumni (Update/Delete)":
    st.header("🔧 Manage Alumni Records")
    
    # Search for alumni to manage
    st.subheader("🔍 Find Alumni to Manage")
    search_id = st.text_input("Enter Alumni ID", placeholder="e.g., 001-2008-09")
    
    col1, col2 = st.columns(2)
    with col1:
        fetch_button = st.button("🔍 Fetch Alumni", use_container_width=True)
    with col2:
        if st.session_state.get("selected_alumni"):
            if st.button("🔄 Clear Selection", use_container_width=True):
                st.session_state["selected_alumni"] = None
                st.rerun()
    
    if fetch_button and search_id:
        try:
            resp = requests.get(f"{API_URL}/alumni/{search_id}")
            if resp.status_code == 200:
                alumni_data = resp.json()
                st.session_state["selected_alumni"] = search_id
                st.success(f"✅ Alumni found: {alumni_data.get('firstname', '')} {alumni_data.get('surname', '')}")
            else:
                st.error("❌ Alumni not found with this ID")
                st.session_state["selected_alumni"] = None
        except Exception as e:
            st.error(f"❌ Error fetching alumni: {str(e)}")
    
    # Show management options if alumni is selected
    if st.session_state.get("selected_alumni"):
        try:
            resp = requests.get(f"{API_URL}/alumni/{st.session_state['selected_alumni']}")
            if resp.status_code == 200:
                d = resp.json()
                
                st.markdown("---")
                st.subheader(f"📋 Managing: {d.get('firstname', '')} {d.get('surname', '')}")
                
                # Show current alumni info
                render_alumni_card(d)
                
                st.markdown("---")
                
                # Management tabs
                tab1, tab2, tab3, tab4 = st.tabs(["✏️ Update Info", "📸 Update Photo", "🆔 Change ID", "🗑️ Delete Alumni"])
                
                # ===== UPDATE INFO TAB =====
                with tab1:
                    st.subheader("✏️ Update Alumni Information")
                    
                    with st.form("update_info_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_firstname = st.text_input("First Name", value=d.get("firstname", ""))
                            new_surname = st.text_input("Surname", value=d.get("surname", ""))
                            new_gender = st.selectbox("Gender", 
                                                    ["Male", "Female", "Other"], 
                                                    index=["Male", "Female", "Other"].index(d.get("gender", "Male")))
                            new_batch = st.text_input("Batch", value=d.get("batch", ""))
                            new_linkedin = st.text_input("LinkedIn URL", value=d.get("linkedin_url", ""))
                        
                        with col2:
                            new_org = st.text_input("Current Organization", value=d.get("current_organization", ""))
                            new_position = st.text_input("Current Position", value=d.get("current_position", ""))
                            new_location = st.text_input("Current Location", value=d.get("current_location", ""))
                            new_experience = st.number_input("Years of Experience", 
                                                           value=float(d.get("Industry_experiences", 0.0)),
                                                           min_value=0.0, max_value=50.0, step=0.5)
                        
                        st.write("**Technical Skills**")
                        col3, col4 = st.columns(2)
                        with col3:
                            new_skill1 = st.text_input("Software Skill 1", value=d.get("software_skill_1", ""))
                            new_skill2 = st.text_input("Software Skill 2", value=d.get("software_skill_2", ""))
                            new_skill3 = st.text_input("Software Skill 3", value=d.get("software_skill_3", ""))
                        
                        with col4:
                            new_lang1 = st.text_input("Programming Language 1", value=d.get("programming_lang_1", ""))
                            new_lang2 = st.text_input("Programming Language 2", value=d.get("programming_lang_2", ""))
                            new_lang3 = st.text_input("Programming Language 3", value=d.get("programming_lang_3", ""))
                        
                        update_info_submit = st.form_submit_button("💾 Update Information", use_container_width=True)
                    
                    if update_info_submit:
                        update_data = {
                            "id": d.get("id"),
                            "firstname": new_firstname,
                            "surname": new_surname or None,
                            "gender": new_gender,
                            "batch": new_batch,
                            "linkedin_url": new_linkedin,
                            "current_organization": new_org or None,
                            "current_position": new_position or None,
                            "current_location": new_location or None,
                            "Industry_experiences": new_experience,
                            "software_skill_1": new_skill1 or None,
                            "software_skill_2": new_skill2 or None,
                            "software_skill_3": new_skill3 or None,
                            "programming_lang_1": new_lang1 or None,
                            "programming_lang_2": new_lang2 or None,
                            "programming_lang_3": new_lang3 or None,
                        }
                        
                        try:
                            update_resp = requests.put(f"{API_URL}/update_alumni/{st.session_state['selected_alumni']}", 
                                                     json=update_data)
                            if update_resp.status_code == 200:
                                st.success("✅ Alumni information updated successfully!")
                                st.rerun()
                            else:
                                st.error(f"❌ Update failed: {update_resp.text}")
                        except Exception as e:
                            st.error(f"❌ Error updating alumni: {str(e)}")
                
                # ===== UPDATE PHOTO TAB =====
                with tab2:
                    st.subheader("📸 Update Profile Photo")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Current Photo:**")
                        if d.get("profile_photo"):
                            try:
                                photo_url = f"{API_URL}/view_photo/{d['id']}"
                                st.image(photo_url, width=200, caption="Current Photo")
                            except:
                                st.info("Could not load current photo")
                        else:
                            st.info("No current photo")
                    
                    with col2:
                        st.write("**Upload New Photo:**")
                        new_photo = st.file_uploader("Choose new photo", type=["jpg", "jpeg", "png"], key="photo_update")
                        
                        if st.button("📸 Update Photo", disabled=not new_photo, use_container_width=True):
                            if new_photo:
                                try:
                                    files = {"new_photo": (new_photo.name, new_photo.getvalue(), new_photo.type)}
                                    photo_resp = requests.put(f"{API_URL}/update-photo/{st.session_state['selected_alumni']}", 
                                                            files=files)
                                    if photo_resp.status_code == 200:
                                        st.success("✅ Photo updated successfully!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Photo update failed: {photo_resp.text}")
                                except Exception as e:
                                    st.error(f"❌ Error updating photo: {str(e)}")
                
                # ===== CHANGE ID TAB =====
                with tab3:
                    st.subheader("🆔 Change Alumni ID")
                    st.warning("⚠️ This will change the alumni's ID based on a new batch year.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"**Current ID:** {d.get('id')}")
                        new_batch_year = st.text_input("New Batch (e.g., 2001-03)", 
                                                     placeholder="YYYY-YY format")
                    
                    with col2:
                        st.write("**⚠️ Important Notes:**")
                        st.write("• This will generate a new sequential ID")
                        st.write("• The old ID will no longer be valid")
                        st.write("• This action cannot be undone")
                    
                    if st.button("🆔 Update Alumni ID", disabled=not new_batch_year, use_container_width=True):
                        if new_batch_year:
                            try:
                                # The API expects the new_batch in the request body
                                update_id_resp = requests.put(
                                    f"{API_URL}/update_id/{st.session_state['selected_alumni']}", 
                                    json={"new_batch": new_batch_year}
                                )
                                if update_id_resp.status_code == 200:
                                    result = update_id_resp.json()
                                    st.success(f"✅ Alumni ID updated successfully! {result.get('message', '')}")
                                    st.session_state["selected_alumni"] = None  # Clear selection since ID changed
                                    st.rerun()
                                else:
                                    st.error(f"❌ ID update failed: {update_id_resp.text}")
                            except Exception as e:
                                st.error(f"❌ Error updating ID: {str(e)}")
                
                # ===== DELETE ALUMNI TAB =====
                with tab4:
                    st.subheader("🗑️ Delete Alumni Record")
                    st.error("⚠️ **Warning:** This action is permanent and cannot be undone!")
                    
                    st.write("**This will permanently delete:**")
                    st.write("• All alumni information")
                    st.write("• Profile photo")
                    st.write("• All associated records")
                    
                    delete_confirmation = st.text_input("Type Top Secret Code to confirm deletion ", placeholder="Only Priyanshu Know this code")
                    
                    if st.button("🗑️ Delete Alumni", 
                               disabled=(delete_confirmation != "DELETE"), 
                               use_container_width=True):
                        if delete_confirmation == "DELETE":
                            try:
                                delete_resp = requests.delete(f"{API_URL}/alumni/{st.session_state['selected_alumni']}")
                                if delete_resp.status_code == 200:
                                    st.success("✅ Alumni deleted successfully!")
                                    st.session_state["selected_alumni"] = None
                                    st.rerun()
                                else:
                                    st.error(f"❌ Delete failed: {delete_resp.text}")
                            except Exception as e:
                                st.error(f"❌ Error deleting alumni: {str(e)}")
            
        except Exception as e:
            st.error(f"❌ Error loading alumni data: {str(e)}")

# =================== FOOTER ===================
st.markdown("---")
st.markdown("*Department of Statistics - Sardar Patel University | Developed by Priyanshu B. Parmar*")




#streamlit run frontend.py
