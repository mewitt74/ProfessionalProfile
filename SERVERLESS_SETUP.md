# Serverless Email Capture Setup

## Deployment Options

### Option 1: Netlify (Recommended - Easiest)

1. **Deploy to Netlify:**
   ```bash
   npm install
   netlify deploy --prod
   ```

2. **Set Environment Variables** in Netlify Dashboard:
   - Go to Site Settings → Environment Variables
   - Add: `EMAIL_USER` = `mwittespencer@gmail.com`
   - Add: `EMAIL_PASSWORD` = `20IndianHackers!`

3. **Generate Gmail App Password:**
   - Go to Google Account → Security → 2-Step Verification
   - At bottom: App passwords → Generate
   - Use this 16-character password (not your regular Gmail password)

4. **Update form action** in index.html:
   ```html
   action="/.netlify/functions/capture-email"
   ```

5. **Test:** Submit the form and check your email!

---

### Option 2: AWS Lambda + API Gateway

1. **Create Lambda Function:**
   - Copy code from `netlify/functions/capture-email.js`
   - Add `nodemailer` layer or package dependencies
   - Set environment variables in Lambda console

2. **Create API Gateway:**
   - Create new REST API
   - Add POST method to `/capture-email`
   - Connect to Lambda function
   - Enable CORS
   - Deploy to stage

3. **Update form** to use API Gateway URL:
   ```html
   action="https://your-api-id.execute-api.region.amazonaws.com/prod/capture-email"
   ```

---

### Option 3: Vercel Serverless Functions

1. **Create `/api/capture-email.js`:**
   ```javascript
   const nodemailer = require('nodemailer');

   export default async function handler(req, res) {
       if (req.method !== 'POST') {
           return res.status(405).json({ error: 'Method not allowed' });
       }
       
       // ... rest of email logic
   }
   ```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

3. **Update form:**
   ```html
   action="/api/capture-email"
   ```

---

## Alternative: SendGrid (No SMTP setup needed)

1. **Install SendGrid:**
   ```bash
   npm install @sendgrid/mail
   ```

2. **Update function:**
   ```javascript
   const sgMail = require('@sendgrid/mail');
   sgMail.setApiKey(process.env.SENDGRID_API_KEY);
   
   await sgMail.send({
       to: 'melissaspencer2@msn.com',
       from: 'verified-sender@yourdomain.com',
       subject: 'New Profile Interest',
       html: emailContent
   });
   ```

3. **Get API Key:**
   - Sign up at sendgrid.com (free tier: 100 emails/day)
   - Settings → API Keys → Create API Key
   - Add to environment variables: `SENDGRID_API_KEY`

---

## Testing Locally

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Set local env variables
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"

# Run local dev server
netlify dev
```

Visit `http://localhost:8888` to test!

---

## Current Setup

Your form currently uses **FormSubmit.co** (free, no backend):
- Works immediately, no setup required
- First time: You'll get verification email
- After verification: All submissions go to your email

To switch to serverless function:
1. Choose deployment option above
2. Update form `action` attribute in index.html
3. Add JavaScript fetch() call instead of direct form submission
