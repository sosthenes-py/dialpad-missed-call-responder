<h1>📞 Dialpad Missed Call Auto SMS Responder</h1>

<p>
  This project is a lightweight <strong>FastAPI</strong> application designed to integrate with the <strong>Dialpad API</strong>. 
  It creates webhooks, starts up <em>call event</em> subscriptions, listens for <em>missed call</em> events via the webhook and automatically sends a predefined <strong>SMS</strong> message 
  to the caller.
</p>

<h2>🚀 Features</h2>
<ul>
  <li>Webhook endpoint for receiving Dialpad missed call events</li>
  <li>Automated SMS response for each missed call</li>
  <li>Configurable SMS message template</li>
  <li>Lightweight, async architecture using FastAPI</li>
</ul>

<h2>🔧 Tech Stack</h2>
<ul>
  <li>Python 3.10+</li>
  <li>FastAPI</li>
  <li>Uvicorn (for ASGI server)</li>
  <li>Dialpad API</li>
  <li>*Docker Support is underway</li>
</ul>

<h2>📦 Installation</h2>
<pre>
git clone https://github.com/sosthenes-py/dialpad-missed-call-responder.git
cd dialpad-missed-call-responder
pip install -r requirements.txt
</pre>

<h2>⚙️ Configuration</h2>
<p>
  Create a <code>.env</code> file with the following environment variables:
</p>
<pre>
DIALPAD_API_KEY=your_dialpad_api_key
DIALPAD_SECRET=any_secret_key_to_validate_webhook_requests
SMS_MESSAGE=Thank you for calling. Sorry we missed your call – we’ll get back to you shortly!
</pre>

<h2>🏃 Running the App</h2>
<pre>
uvicorn main:app --reload
</pre>

<h2>🧪 Testing</h2>
<p>Due to API limitations, testing with a live Dialpad environment is recommended for full functionality.</p>

<h2>📄 License</h2>
<p>This project is open source and available under the <strong>MIT License</strong>.</p>
