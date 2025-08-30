#!/bin/bash

# 1. Activate virtualenv
source venv/bin/activate

# 2. Start ngrok for Streamlit (port 8501) in background
echo "Starting ngrok..."
ngrok http 8501 > /dev/null &
NGROK_PID=$!

# 3. Wait for ngrok to be ready
until curl -s http://127.0.0.1:4040/api/tunnels | grep -q "ngrok-free.app"; do
  sleep 0.5
done

# 4. Get public ngrok URL
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | \
  grep -o '"https://[0-9a-z]*\.ngrok-free\.app"' | head -n 1 | sed 's/"//g')

# 5. Display the public link
echo "✅ Your app is live at:"
echo "$NGROK_URL"
echo

# 6. Start Streamlit
streamlit run app.py &
STREAMLIT_PID=$!
wait $STREAMLIT_PID

# 7. Kill ngrok when Streamlit finishes
kill $NGROK_PID
echo "Ngrok terminated."