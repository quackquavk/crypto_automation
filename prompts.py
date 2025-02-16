from langchain_core.prompts import PromptTemplate
from langchain_ollama import 

PROMPT_TEMPLATE_EMAIL = """
<input>
{coin_names}
</input>

You are an expert financial analyst specializing in cryptocurrency market trends and sentiment analysis. Your task is to analyze 20 Reddit posts related to the given crypto coins and determine the overall market sentiment (positive, neutral, or negative). Consider key aspects such as community discussions, expert opinions, major news, recent developments, and social engagement.

<instructions>
<1> **Analyze Sentiment**: Extract insights from the posts, considering the tone, language, and recurring themes.
<2> **Summarize Key Points**: Identify the major concerns, opportunities, and trends discussed in the community.
<3> **Generate an Email Report**:
   - Begin with a **brief, professional introduction** stating the purpose of the email.
   - Provide an **overview of the findings**, summarizing the general sentiment.
   - Highlight **notable positive or negative trends**, supported by specific observations.
   - Offer a **conclusion** with an actionable recommendation (e.g., watch closely, potential growth, high volatility).
   - Maintain a professional, concise, and engaging tone.

Ensure the email is structured, clear, and easy to digest for the client.

</instructions>

<output_format>
**Subject:** Market Sentiment Analysis for {coin_names}

**Dear [Client's Name],**

I hope you're doing well. Below is the latest market sentiment analysis based on 20 Reddit discussions regarding {coin_names}.

**Summary of Market Sentiment:**  
[State whether the overall sentiment is positive, neutral, or negative.]

**Key Insights:**  
- [Insight #1: Noteworthy discussion points, such as strong bullish sentiment due to a new partnership, upcoming upgrade, or regulatory news.]
- [Insight #2: Any concerns, such as FUD (Fear, Uncertainty, Doubt), community skepticism, or security issues.]
- [Insight #3: Potential growth indicators or warning signs based on engagement and user sentiment.]

**Conclusion & Recommendation:**  
Based on this analysis, we recommend [actionable advice such as monitoring the market, potential buying/selling opportunities, or caution against volatility].

Please let me know if you’d like a deeper dive into any specific aspect.

Best regards,  
[Your Name]  
[Your Position]  
[Your Contact Information]  

</output_format>
"""
