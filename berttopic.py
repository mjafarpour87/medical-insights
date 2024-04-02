from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

# Sample text data
text_data = ["Your text paragraph here", "Another text paragraph",
             "PURPOSE:Adherence to oral endocrine therapy (ET) remains an issue for up to half of women prescribed these medications. There is emerging data that Black breast cancer survivors (BCS) have lower rates of ET adherence. Given the disparities in breast cancer recurrence and survival for Black BCS compared to their White counterparts, the goal of this study is to better understand barriers to ET adherence among Black BCS from the patient and provider perspectives. METHODS:In this qualitative study, we conducted semi-structured interviews between October 29, 2021, and March 1, 2023. Interviews were recorded and transcribed, and coded data were organized into primary and secondary themes. Participants were recruited from a single academic cancer center. A convenience sample of 24 Black BCS and 9 medical oncology providers was included. Eligible BCS were 18 years or older, English-speaking, diagnosed with stage I-III hormone receptor-positive breast cancer, who had initiated ET. RESULTS:Mean age of the BCS was 55 years (interquartile range, IQR 17 years). About one-fourth had a high school diploma or less (26.1%) and 47% completed a college education or higher. Approximately one-third of participants had annual household incomes of $40,000 or less (30.4%) or more than $100,000 (30.4%). Forty-three percent of the patient participants had private insurance; 11% were insured through Medicaid or the federal healthcare exchange; 26.1% had Medicare; and 13% were uninsured. Of the 9 medical oncology providers interviewed, 2 were advanced practice providers, and 7 were medical oncologists. We found 3 major themes: (1) Black BCS often had concerns about ET before initiation; (2) after initiation, both BCS and providers reported side effects as the most impactful barrier to ET adherence; and (3) survivors experienced challenges with managing ET side effects. CONCLUSIONS:Our results suggest that multifaceted support interventions for managing ET-related symptoms may lead to improved adherence to ET among Black women and may reduce disparities in outcomes. IMPLICATIONS FOR CANCER SURVIVORS:Multifaceted support interventions for managing ET-related symptoms may lead to improved adherence to ET among Black breast cancer survivors.",
             ]

# Initialize BERTopic model
model = BERTopic()

# Fit BERTopic model on text data
topics, _ = model.fit_transform(text_data)

# Get the topics and their corresponding keywords
topic_keywords = model.get_topics()

# Print the topics and their keywords
for topic, keywords in topic_keywords.items():
    print(f"Topic {topic}: {', '.join(keywords)}")
