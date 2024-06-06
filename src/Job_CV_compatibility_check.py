import streamlit as st
import os
import data_processing as dp

results = {}

def resume_processing(resume,jd):
    print('------------------------------------------------------------------')

    #Getting resume filename from data/resume directory
    resume_file_name = 'data/resume/' + str(resume)
    print('Resume found: ', resume_file_name)

    #Getting JD filelist from data/jd directory
    print('JD file list found: ', jd)

    for file_name in jd:
        #==========================================================================
        #------------Keywords extraction from JD using spacy---------------------
        jd_file_name = 'data/jd/' + str(file_name.name)
        data_jd = dp.data_load(jd_file_name)
        keywords_jd = dp.spacy_keywords(data_jd)

        #==========================================================================
        #---------------Keywords extraction from resume using nltk---------------------
        data_resume = dp.data_load(resume_file_name)
        keywords_resume = dp.nltk_keywords(data_resume)

        #==========================================================================
        #----------------Matching Keywords between JD and Resume-----------------------

        #Creating a table showing Match Result between JD and Resume
        jd_keywords_in_resume_table = []
        for word in keywords_jd:
            if word in keywords_resume:
                match_result = [word, 'Match']
            else:
                match_result = [word, 'No Match']
            jd_keywords_in_resume_table.append(match_result)

        from tabulate import tabulate
        print(f'Comparing Resume and {file_name.name}:')
        print(tabulate( jd_keywords_in_resume_table, headers=['Serial', 'JD Keyword', 'JD-Resume Match Result'], showindex='always', tablefmt='psql' ))

        #==========================================================================
        #Calculating the percentage of the match result
        jd_keywords_in_resume_list = [w for w in keywords_jd if w in keywords_resume]
        jd_keywords_in_resume_list_count = len(jd_keywords_in_resume_list)
        jd_keywords_count_total = len(keywords_jd)
        

        matchPercentage = (jd_keywords_in_resume_list_count/jd_keywords_count_total) * 100
        matchPercentage = round(matchPercentage, 2) # round to two decimal
        print( f'Match percentage based on Keywords: {matchPercentage}%')

        #==========================================================================
        #--------------Cosine Similarity between JD and Resume Keywords----------------
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        # A list of text
        text = [data_jd, data_resume]

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)

        #get the match percentage
        matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
        matchPercentage = round(matchPercentage, 2) # round to two decimal
        print( f'Match percentage based on Cosine Similarity: {matchPercentage}%')
        
        if file_name.name not in results:
            results[str(file_name.name)] = []
            results[str(file_name.name)].append([resume, matchPercentage])
        else:
            results[str(file_name.name)].append([resume, matchPercentage])


# Create the necessary directories if they do not exist
os.makedirs('data/resume', exist_ok=True)
os.makedirs('data/jd', exist_ok=True)

# Streamlit file uploader for resume and job description
st.title("Resume and Job Description Uploader")

resume_files = st.file_uploader("Upload Resume", type=["txt"],accept_multiple_files=True)
jd_files = st.file_uploader("Upload Job Description", type=["txt"],accept_multiple_files=True)
results = {}

for resume in resume_files:
    if resume is not None:
        resume_file_name = os.path.join('data/resume', resume.name)
        with open(resume_file_name, 'wb') as fp:
            fp.write(resume.getbuffer())
        st.success(f"Resume uploaded: {resume.name}")

for jd in jd_files:
    if jd is not None:
        jd_file_name = os.path.join('data/jd', jd.name)
        with open(jd_file_name, 'wb') as fp:
            fp.write(jd.getbuffer())
        st.success(f"Job description uploaded: {jd.name}")

if st.button('Process Resume and JD'):
    if resume_files is not None and jd_files is not None:
        for resume in resume_files:
            resume_processing(resume.name,jd_files)
        st.session_state.page = 'results'
    else:
        st.error("Please upload both resume and job description files.")

results = {key: sorted(value, key=lambda x: x[1], reverse=True) for key, value in results.items()}
st.session_state.results = []
st.session_state.results.append(results)
print(results)

if 'page' in st.session_state and st.session_state.page == 'results':
    st.title("Processing Results")
    if 'results' in st.session_state:
        for jd, resumes in results.items():
            st.header(f"Job Description: {jd}")
            for resume, score in resumes:
                st.write(f"Resume: {resume} - Score: {score}")
    if st.button('Back'):
        st.session_state.page = 'upload'
else:
    st.title("Resume and Job Description Uploader")