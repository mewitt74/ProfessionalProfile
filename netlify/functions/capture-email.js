// Netlify Serverless Function for Email Capture
// Deploy this to Netlify Functions or adapt for AWS Lambda/Vercel

const nodemailer = require('nodemailer');

exports.handler = async (event, context) => {
    // Only allow POST requests
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const { email, name, message } = JSON.parse(event.body);

        // Validate email
        if (!email || !email.includes('@')) {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'Valid email is required' })
            };
        }

        // Configure your email service
        // Option 1: Using Gmail (requires app password)
        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.EMAIL_USER, // Your Gmail address
                pass: process.env.EMAIL_PASSWORD // Gmail app password
            }
        });

        // Option 2: Using SendGrid
        // const sgMail = require('@sendgrid/mail');
        // sgMail.setApiKey(process.env.SENDGRID_API_KEY);

        // Email content
        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: 'melissaspencer2@msn.com',
            subject: '🎯 New Professional Profile Interest!',
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #667eea; border-radius: 8px;">
                    <h2 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">New Profile Inquiry</h2>
                    
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 6px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📧 Email:</strong> ${email}</p>
                        ${name ? `<p style="margin: 5px 0;"><strong>👤 Name:</strong> ${name}</p>` : ''}
                        ${message ? `<p style="margin: 5px 0;"><strong>💬 Message:</strong><br>${message}</p>` : ''}
                        <p style="margin: 5px 0;"><strong>🕐 Timestamp:</strong> ${new Date().toLocaleString()}</p>
                    </div>
                    
                    <p style="color: #666; font-size: 14px; margin-top: 20px;">
                        This inquiry was submitted from your professional profile at 
                        <a href="https://mewitt74.github.io/ProfessionalProfile/" style="color: #667eea;">mewitt74.github.io/ProfessionalProfile</a>
                    </p>
                </div>
            `
        };

        // Send email
        await transporter.sendMail(mailOptions);

        // Optionally: Store in database
        // await storeInDatabase({ email, name, message, timestamp: new Date() });

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            body: JSON.stringify({ 
                success: true, 
                message: 'Thank you! You\'ve been added to my network.' 
            })
        };

    } catch (error) {
        console.error('Email capture error:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ 
                error: 'Failed to process request',
                details: error.message 
            })
        };
    }
};
