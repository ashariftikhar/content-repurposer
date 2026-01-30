import streamlit as st
import re
import random
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="AI Content Repurposer",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .idea-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .platform-tag {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎬 AI Content Repurposer v1.0</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", width=100)
    st.title("Settings")
    
    example_urls = {
        "Tech Tutorial": "https://youtu.be/dQw4w9WgXcQ",
        "AI Guide": "https://youtube.com/watch?v=abc123def45",
        "Programming": "https://youtu.be/xyz789uvw01"
    }
    
    selected_example = st.selectbox("Try example:", list(example_urls.keys()))
    if st.button("Load Example"):
        st.session_state.youtube_url = example_urls[selected_example]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📥 Enter YouTube URL")
    youtube_url = st.text_input(
        "YouTube URL:",
        placeholder="https://www.youtube.com/watch?v=... or https://youtu.be/...",
        key="youtube_url",
        label_visibility="collapsed"
    )

def extract_video_id(url):
    """Extract YouTube video ID"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([\w-]{11})',
        r'(?:youtu\.be\/)([\w-]{11})',
        r'(?:youtube\.com\/embed\/)([\w-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title(video_id):
    """Mock function - real version uses YouTube API"""
    titles = [
        "How to Build AI Tools in 2024 - Complete Guide",
        "Python Automation: 10 Weekend Projects",
        "The Future of AI in Content Creation",
        "Master Web Scraping with Python",
        "Build Your First SaaS in 30 Days"
    ]
    random.seed(video_id)
    return random.choice(titles)

def generate_content_ideas(topic, video_id):
    """Generate content ideas for different platforms"""
    
    ideas = [
        {
            "platform": "Twitter",
            "emoji": "🐦",
            "title": f"Twitter Thread: 5 Key Points from '{topic}'",
            "description": "Break down complex concepts into tweet-sized insights perfect for virality.",
            "hashtags": ["#AI", "#Tech", "#Learn"],
            "steps": ["Outline key points", "Add data/statistics", "Include questions for engagement"]
        },
        {
            "platform": "LinkedIn",
            "emoji": "💼",
            "title": f"LinkedIn Article: Professional Take on '{topic}'",
            "description": "Position yourself as an expert with well-researched insights for professionals.",
            "hashtags": ["#Career", "#Professional", "#Industry"],
            "steps": ["Start with hook", "Add case studies", "Include actionable tips"]
        },
        {
            "platform": "Blog",
            "emoji": "✍️",
            "title": f"Comprehensive Guide: '{topic}' Explained",
            "description": "In-depth tutorial with examples, perfect for SEO and organic traffic.",
            "hashtags": ["#Tutorial", "#HowTo", "#Guide"],
            "steps": ["Create outline", "Add code examples", "Include screenshots"]
        },
        {
            "platform": "Instagram",
            "emoji": "📸",
            "title": f"Instagram Carousel: Visual Guide to '{topic}'",
            "description": "High-engagement visual content that simplifies complex topics.",
            "hashtags": ["#Visual", "#Design", "#EduGram"],
            "steps": ["Design 10 slides", "Add visuals", "Write captions"]
        },
        {
            "platform": "Newsletter",
            "emoji": "📧",
            "title": f"Newsletter Deep Dive: '{topic}'",
            "description": "Exclusive content for subscribers with deep analysis and resources.",
            "hashtags": ["#Newsletter", "#Exclusive", "#DeepDive"],
            "steps": ["Write introduction", "Add resources", "Include CTAs"]
        },
        {
            "platform": "TikTok",
            "emoji": "🎵",
            "title": f"TikTok Series: '{topic}' in 60 Seconds",
            "description": "Snackable video content with high virality potential.",
            "hashtags": ["#TikTok", "#ShortForm", "#EduTok"],
            "steps": ["Script 3 videos", "Record clips", "Add text overlays"]
        }
    ]
    
    # Shuffle based on video_id for variety
    random.seed(sum(ord(c) for c in video_id))
    random.shuffle(ideas)
    
    return ideas

# Process button
if st.button("🚀 Generate Content Ideas", type="primary", use_container_width=True):
    if youtube_url:
        with st.spinner("Processing YouTube URL..."):
            video_id = extract_video_id(youtube_url)
            
            if video_id:
                st.success(f"✅ Video ID extracted: `{video_id}`")
                
                # Get title
                title = get_video_title(video_id)
                st.info(f"📹 **Video Title:** {title}")
                
                # Generate ideas
                with st.spinner("Generating content ideas..."):
                    ideas = generate_content_ideas(title, video_id)
                
                # Display results
                st.markdown("---")
                st.subheader(f"🎯 Generated {len(ideas)} Content Ideas")
                
                for i, idea in enumerate(ideas, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="idea-card">
                            <h3>{idea['emoji']} Idea #{i}: {idea['title']}</h3>
                            <p><strong>Platform:</strong> {idea['platform']}</p>
                            <p>{idea['description']}</p>
                            <div>
                                {" ".join([f'<span class="platform-tag">{tag}</span>' for tag in idea["hashtags"]])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander(f"📋 Action Steps for {idea['platform']}"):
                            for j, step in enumerate(idea['steps'], 1):
                                st.write(f"{j}. {step}")
                
                # Download option
                ideas_json = json.dumps(ideas, indent=2)
                st.download_button(
                    label="📥 Download Ideas as JSON",
                    data=ideas_json,
                    file_name=f"content_ideas_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
                
                # Stats
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Ideas", len(ideas))
                with col2:
                    st.metric("Platforms", len(set(i['platform'] for i in ideas)))
                with col3:
                    st.metric("Generated", datetime.now().strftime("%H:%M"))
                
            else:
                st.error("❌ Invalid YouTube URL. Please check the format.")
    else:
        st.warning("⚠️ Please enter a YouTube URL first.")

with col2:
    st.markdown("### 📚 How to Use")
    st.markdown("""
    1. **Paste** any YouTube URL
    2. **Click** Generate button
    3. **Get** 6 content ideas
    4. **Download** as JSON
    
    ### 🎯 Perfect For:
    - Content creators
    - Social media managers
    - YouTubers
    - Marketers
    - AI enthusiasts
    """)

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Part of 270-day AI Tool Challenge | Deploy on Vercel")