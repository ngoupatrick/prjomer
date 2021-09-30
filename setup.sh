mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor=\"#FF7903\" \n\
backgroundColor=\"#0E1117\" \n\
secondaryBackgroundColor=\"#31333F\" \n\
textColor=\"#FAFAFA\" \n\
font=\"sans serif\" \n\
\n\
" > ~/.streamlit/config.toml
