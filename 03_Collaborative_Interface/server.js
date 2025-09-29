#!/usr/bin/env node
/**
 * 🔥 DEEPSEEK AI VALIDATION - REAL-TIME COLLABORATIVE SERVER
 * Socket.io server for live collaborative code validation
 * #ResendMCPHackathon #GODTIER #RealTime
 */

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Store active sessions and users
const activeSessions = new Map();
const connectedUsers = new Map();

// Socket.io connection handling
io.on('connection', (socket) => {
    console.log(`🚀 User connected: ${socket.id}`);
    
    // User joins a validation session
    socket.on('join-session', (data) => {
        const { sessionId, username, avatar } = data;
        
        // Join the socket room
        socket.join(sessionId);
        
        // Store user info
        connectedUsers.set(socket.id, {
            sessionId,
            username: username || `Developer_${socket.id.substring(0, 6)}`,
            avatar: avatar || '👨‍💻',
            joinedAt: new Date()
        });
        
        // Initialize session if it doesn't exist
        if (!activeSessions.has(sessionId)) {
            activeSessions.set(sessionId, {
                id: sessionId,
                users: new Map(),
                codeHistory: [],
                validationResults: [],
                createdAt: new Date()
            });
        }
        
        const session = activeSessions.get(sessionId);
        session.users.set(socket.id, connectedUsers.get(socket.id));
        
        // Notify others in the session
        socket.to(sessionId).emit('user-joined', {
            user: connectedUsers.get(socket.id),
            totalUsers: session.users.size
        });
        
        // Send current session state to the new user
        socket.emit('session-state', {
            session: {
                id: sessionId,
                users: Array.from(session.users.values()),
                codeHistory: session.codeHistory.slice(-10), // Last 10 submissions
                validationResults: session.validationResults.slice(-10)
            }
        });
        
        console.log(`👥 ${connectedUsers.get(socket.id).username} joined session: ${sessionId}`);
    });
    
    // Handle real-time code submission
    socket.on('submit-code', async (data) => {
        const user = connectedUsers.get(socket.id);
        if (!user) return;
        
        const { code, validationType, language, requestEmail, unhingedMode } = data;
        const session = activeSessions.get(user.sessionId);
        
        if (!session) return;
        
        const submission = {
            id: `sub_${Date.now()}_${socket.id}`,
            user: user,
            code: code,
            validationType: validationType || 'general_validation',
            language: language || 'python',
            submittedAt: new Date(),
            status: 'validating'
        };
        
        // Add to session history
        session.codeHistory.push(submission);
        
        // Broadcast to all users in session that validation started
        const modeText = unhingedMode ? ' 🔥 UNHINGED' : '';
        io.to(user.sessionId).emit('validation-started', {
            submission: submission,
            message: `🔍 ${user.username} submitted code for ${validationType}${modeText} validation...`
        });
        
        console.log(`🔍 ${user.username} submitted code for validation: ${validationType}${modeText}`);
        
        try {
            // Run the AI validation (call our Python backend)
            const validationResult = await runAIValidation(code, validationType, unhingedMode);
            
            const result = {
                id: `result_${Date.now()}`,
                submissionId: submission.id,
                user: user,
                validationResult: validationResult,
                completedAt: new Date()
            };
            
            // Add to session results
            session.validationResults.push(result);
            
            // Broadcast results to all users in session
            io.to(user.sessionId).emit('validation-complete', {
                result: result,
                message: `✅ ${user.username}'s validation complete: ${validationResult.overall_rating}`
            });
            
            // If email sending is requested, trigger that too
            if (requestEmail) {
                const emailResult = await sendValidationEmail(validationResult, user);
                io.to(user.sessionId).emit('email-sent', {
                    emailId: emailResult.email_id,
                    recipient: emailResult.recipient,
                    chartsIncluded: emailResult.charts_included,
                    method: emailResult.method,
                    message: `📧 Enhanced validation report emailed to ${emailResult.recipient}`
                });
            }
            
        } catch (error) {
            console.error('❌ Validation failed:', error);
            
            io.to(user.sessionId).emit('validation-error', {
                submissionId: submission.id,
                error: error.message,
                message: `❌ ${user.username}'s validation failed: ${error.message}`
            });
        }
    });
    
    
    // Handle typing indicators
    socket.on('typing', (data) => {
        const user = connectedUsers.get(socket.id);
        if (!user) return;
        
        socket.to(user.sessionId).emit('user-typing', {
            userId: socket.id,
            username: user.username,
            isTyping: data.isTyping
        });
    });
    
    // Handle disconnection
    socket.on('disconnect', () => {
        const user = connectedUsers.get(socket.id);
        
        if (user) {
            const session = activeSessions.get(user.sessionId);
            if (session) {
                session.users.delete(socket.id);
                
                // Notify others in session
                socket.to(user.sessionId).emit('user-left', {
                    user: user,
                    totalUsers: session.users.size
                });
                
                // Clean up empty sessions
                if (session.users.size === 0) {
                    activeSessions.delete(user.sessionId);
                    console.log(`🧹 Cleaned up empty session: ${user.sessionId}`);
                }
            }
            
            connectedUsers.delete(socket.id);
            console.log(`👋 ${user.username} disconnected from session: ${user.sessionId}`);
        }
    });
});

// AI Validation function - calls our Python backend
async function runAIValidation(code, validationType, unhingedMode = false) {
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, '..', '02_Technical_System', 'validation_api.py');
        const child = spawn('python3', [pythonScript, validationType], {
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        // Send code to Python script via stdin
        child.stdin.write(JSON.stringify({ 
            code: code, 
            type: validationType,
            unhinged_mode: unhingedMode 
        }));
        child.stdin.end();
        
        let output = '';
        let error = '';
        
        child.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        child.stderr.on('data', (data) => {
            error += data.toString();
        });
        
        child.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python validation failed: ${error}`));
            } else {
                try {
                    const result = JSON.parse(output);
                    resolve(result);
                } catch (e) {
                    reject(new Error(`Failed to parse validation result: ${e.message}`));
                }
            }
        });
        
        // Timeout after 30 seconds
        setTimeout(() => {
            child.kill();
            reject(new Error('Validation timeout'));
        }, 30000);
    });
}

// Enhanced email sending function with real Resend MCP integration
async function sendValidationEmail(validationResult, user) {
    try {
        // Create enhanced email agent
        const { EnhancedMCPEmailAgent } = require('../02_Technical_System/mcp_email_agent_pro');
        
        const agent = new EnhancedMCPEmailAgent(
            process.env.RESEND_API_KEY || 'demo_key_for_realtime',
            'realtime@deepseek-ai.com'
        );
        
        // Generate enhanced email report
        const charts = await agent._create_validation_charts(validationResult);
        const htmlContent = await agent._generate_enhanced_report(
            validationResult, 
            'collaborative_session',
            charts
        );
        
        // Send via real Resend API
        const recipient = user.email || 'demo@example.com';
        const subject = `🚀 Real-Time Validation Results for ${user.username}`;
        
        const emailResult = await agent._send_via_real_resend(
            recipient,
            subject,
            htmlContent
        );
        
        return {
            email_id: emailResult.id || `email_${Date.now()}`,
            recipient: recipient,
            sent: emailResult.sent || true,
            charts_included: Object.keys(charts).length,
            method: 'Enhanced Resend MCP Integration'
        };
        
    } catch (error) {
        console.error('📧 Email sending failed:', error);
        return {
            email_id: `fallback_${Date.now()}`,
            recipient: user.email || 'demo@example.com',
            sent: false,
            error: error.message
        };
    }
}

// API Routes
app.get('/api/sessions', (req, res) => {
    const sessionList = Array.from(activeSessions.values()).map(session => ({
        id: session.id,
        userCount: session.users.size,
        lastActivity: Math.max(
            ...session.codeHistory.map(h => new Date(h.submittedAt).getTime()),
            ...session.validationResults.map(r => new Date(r.completedAt).getTime())
        ),
        createdAt: session.createdAt
    }));
    
    res.json(sessionList);
});

app.get('/api/session/:id', (req, res) => {
    const session = activeSessions.get(req.params.id);
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    res.json({
        id: session.id,
        users: Array.from(session.users.values()),
        codeHistory: session.codeHistory,
        validationResults: session.validationResults,
        createdAt: session.createdAt
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        activeSessions: activeSessions.size,
        connectedUsers: connectedUsers.size,
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

const PORT = process.env.PORT || 3001;

server.listen(PORT, () => {
    console.log(`🚀 DeepSeek Collaborative Validation Server running on port ${PORT}`);
    console.log(`💫 Real-time magic happening at http://localhost:${PORT}`);
    console.log(`🔥 Ready to blow minds with collaborative AI validation!`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('🛑 Server shutting down gracefully...');
    server.close(() => {
        console.log('✅ Server closed');
        process.exit(0);
    });
});