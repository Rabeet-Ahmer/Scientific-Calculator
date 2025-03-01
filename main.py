import os
import streamlit as st
from dotenv import load_dotenv
import wolframalpha

load_dotenv()
API_KEY = os.getenv("WOLFRAM_API_KEY")
client = wolframalpha.Client(API_KEY)

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="https://cdn-icons-png.flaticon.com/512/891/891175.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

def styling():
    st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background-color: #0e1117;
            padding: 20px;
        }
        
        /* Header styling */
        h1 {
            color: #2c3e50 !important;
            background: linear-gradient(120deg, #f6f8fa, #ffffff);
            font-family: 'Helvetica Neue', sans-serif;
            text-align: center;
            padding: 20px;
            margin: 20px 0;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            font-weight: 600;
            letter-spacing: 0.5px;
            border: 1px solid rgba(0,0,0,0.1);
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #6b7fd7;
            padding: 10px;
            font-size: 16px;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
            color: white;
        }
        
        .stButton > button:active {
            transform: translateY(0px);
            box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
        }
        
        /* Results container */
        .results-container {
            background: rgba(255, 255, 255, 0.95);
            background: linear-gradient(169deg, rgba(255, 255, 255, 0.95) 0%, rgba(243, 244, 246, 0.95) 100%);
            padding: 30px;
            border-radius: 24px;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.05),
                0 10px 20px rgba(99, 102, 241, 0.04),
                inset 0 0 80px rgba(255, 255, 255, 0.5);
            margin: 30px 0;
            border: 1px solid rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .results-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: -50%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                to right,
                rgba(255, 255, 255, 0.8),
                transparent
            );
            transform: skewX(-25deg);
            transition: 0.75s;
            opacity: 0;
        }

        .results-container:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.08),
                0 15px 30px rgba(99, 102, 241, 0.07),
                inset 0 0 80px rgba(255, 255, 255, 0.6);
        }

        .results-container:hover::before {
            animation: shine 1.5s ease-out;
            opacity: 1;
        }

        @keyframes shine {
            0% {
                left: -50%;
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            100% {
                left: 150%;
                opacity: 0;
            }
        }

        .results-container p {
            color: #2c3e50;
            font-size: 18px;
            font-weight: 500;
            line-height: 1.8;
            margin: 12px 0;
            font-family: 'Helvetica Neue', sans-serif;
            letter-spacing: 0.3px;
            position: relative;
            z-index: 1;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #f1f3f8;
        }
        
        /* Example chip styling */
        .examples {
            display: inline-block;
            background-color: #e0e5ff;
            color: #3a4b8c;
            padding: 8px 15px;
            border-radius: 20px;
            margin: 5px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .examples:hover {
            background-color: #d0d8ff;
        }
                
    </style>
    """, unsafe_allow_html=True)

def setup_page():
    """Configure the Streamlit page layout and header."""
    st.markdown("<h1>Scientific Calculator 🌌</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle" style='
            text-align: center;
            font-size: 18px;
            color: #4a5568;
            font-family: "Helvetica Neue", sans-serif;
            margin: 15px auto;
            letter-spacing: 0.3px;
            background: linear-gradient(120deg, #3a4f7a, #2d3748);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 500;
            padding: 10px;
        '>
            ✨ Solves any problem using AI 🚀
        </p>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Sidebar content
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/891/891175.png", width=100 )
    st.sidebar.markdown("### 💡 Tips & Examples:")
    
    # Example chips in sidebar 
    examples = [
        "2+2", 
        "sqrt(16)", 
        "solve 2x + 5 = 15", 
        "integrate x^2 from 0 to 1",
        "derivative of x^3",
        "factor x^2 - 4"
    ]
    
    # Display examples 
    for i, example in enumerate(examples):
        if st.sidebar.button(example, key=f"example_{i}"):
            st.session_state.equation = example


def get_solution(equation: str) -> str:
    """Get solution from Wolfram Alpha API."""
    try:
            
        res = client.query(equation)
        answer = next(res.results).text
        return answer
    except Exception as e:
        return f"Could not compute the answer: {str(e)}"

def main():
    """Main application function."""
    styling()
    setup_page()
    
    # Initialize session state for equation if it doesn't exist
    if 'equation' not in st.session_state:
        st.session_state.equation = ""
    
    # Main calculator container
    with st.container():
        st.markdown('<div style="max-width: 800px; margin: 0 auto; padding: 20px;">', unsafe_allow_html=True)
        
        # User input with session state
        equation = st.text_input(
            "Enter your equation or mathematical expression:", 
            value=st.session_state.equation,
            placeholder="Type your equation here..."
        )
        
        # Update session state
        st.session_state.equation = equation
        
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            calculate_button = st.button("Calculate", key="calc_button", type="primary")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Process calculation
        if calculate_button:
            if not equation:
                st.warning("⚠️ Please enter an equation first!")
                return
                
            try:
                with st.spinner("Calculating..."):
                    answer = get_solution(equation)
                    st.success("Calculation completed!")
                    st.markdown(f'<div class="results-container"><h3 style="color: black">Result</h3><p>Answer: {answer}</p></div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()