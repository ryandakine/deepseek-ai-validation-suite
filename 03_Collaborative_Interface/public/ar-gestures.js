/**
 * 🤯 AR GESTURE RECOGNITION - DEEPSEEK AI VALIDATION
 * Wave your hands to write code in the air!
 * Uses webcam and MediaPipe for real-time hand tracking
 * #ResendMCPHackathon #AR #GODTIER #MindBlown
 */

class ARGestureCodeInput {
    constructor() {
        this.isEnabled = false;
        this.isTracking = false;
        this.videoElement = null;
        this.canvasElement = null;
        this.ctx = null;
        this.hands = null;
        this.gestureBuffer = [];
        this.currentCode = '';
        this.lastGestureTime = 0;
        this.gestureHistory = [];
        
        // Gesture patterns for code snippets
        this.gesturePatterns = {
            'function_def': {
                pattern: 'down-right-down',
                code: 'def function_name():\n    pass',
                description: '📝 Function Definition'
            },
            'if_statement': {
                pattern: 'up-right-down',
                code: 'if condition:\n    # code here\nelse:\n    # alternative',
                description: '🔀 If Statement'
            },
            'crypto_import': {
                pattern: 'circle-right',
                code: 'from decimal import Decimal, getcontext\nfrom cryptography.fernet import Fernet',
                description: '🏦 Crypto Imports'
            },
            'security_scan': {
                pattern: 'zigzag',
                code: 'import nmap\nimport socket\n# Security scanning code',
                description: '🔒 Security Scan'
            },
            'betting_calc': {
                pattern: 'up-down-up',
                code: 'def kelly_criterion(win_prob, odds):\n    return (win_prob * odds - 1) / odds',
                description: '🎲 Kelly Criterion'
            },
            'clear_code': {
                pattern: 'left-right-left',
                code: '',
                description: '🧹 Clear Code'
            }
        };
    }
    
    async init() {
        try {
            console.log('🤯 Initializing AR Gesture Recognition...');
            
            // Load MediaPipe Hands
            await this.loadMediaPipeHands();
            
            // Setup video capture
            await this.setupVideoCapture();
            
            // Initialize gesture detection
            this.initializeGestureDetection();
            
            this.isEnabled = true;
            console.log('✅ AR Gesture Recognition ready!');
            console.log('🤘 Wave your hands to write code in the air!');
            
            return true;
        } catch (error) {
            console.error('❌ AR Gesture Recognition failed to initialize:', error);
            return false;
        }
    }
    
    async loadMediaPipeHands() {
        // Load MediaPipe Hands via CDN
        return new Promise((resolve, reject) => {
            if (window.Hands) {
                resolve();
                return;
            }
            
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1646424915/hands.js';
            script.onload = () => {
                console.log('📦 MediaPipe Hands loaded');
                resolve();
            };
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    async setupVideoCapture() {
        // Create video element for webcam
        this.videoElement = document.createElement('video');
        this.videoElement.style.display = 'none';
        this.videoElement.autoplay = true;
        this.videoElement.muted = true;
        document.body.appendChild(this.videoElement);
        
        // Create canvas for drawing hand landmarks
        this.canvasElement = document.createElement('canvas');
        this.canvasElement.id = 'ar-gesture-canvas';
        this.canvasElement.style.position = 'fixed';
        this.canvasElement.style.top = '10px';
        this.canvasElement.style.right = '10px';
        this.canvasElement.style.width = '300px';
        this.canvasElement.style.height = '200px';
        this.canvasElement.style.border = '2px solid #00ff88';
        this.canvasElement.style.borderRadius = '10px';
        this.canvasElement.style.zIndex = '1000';
        this.canvasElement.style.background = 'rgba(0, 20, 40, 0.9)';
        this.canvasElement.width = 300;
        this.canvasElement.height = 200;
        document.body.appendChild(this.canvasElement);
        
        this.ctx = this.canvasElement.getContext('2d');
        
        // Get webcam access
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 }
        });
        this.videoElement.srcObject = stream;
        
        await new Promise((resolve) => {
            this.videoElement.onloadedmetadata = resolve;
        });
    }
    
    initializeGestureDetection() {
        // Initialize MediaPipe Hands
        this.hands = new Hands({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1646424915/${file}`;
            }
        });
        
        this.hands.setOptions({
            maxNumHands: 2,
            modelComplexity: 1,
            minDetectionConfidence: 0.7,
            minTrackingConfidence: 0.5
        });
        
        this.hands.onResults((results) => {
            this.processHandResults(results);
        });
        
        // Start processing video frames
        this.processFrame();
    }
    
    async processFrame() {
        if (this.videoElement && this.hands) {
            await this.hands.send({ image: this.videoElement });
        }
        requestAnimationFrame(() => this.processFrame());
    }
    
    processHandResults(results) {
        // Clear canvas
        this.ctx.fillStyle = 'rgba(0, 20, 40, 0.9)';
        this.ctx.fillRect(0, 0, this.canvasElement.width, this.canvasElement.height);
        
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            for (let i = 0; i < results.multiHandLandmarks.length; i++) {
                const landmarks = results.multiHandLandmarks[i];
                const handedness = results.multiHandedness[i];
                
                // Draw hand landmarks
                this.drawHandLandmarks(landmarks, handedness.label);
                
                // Detect gestures
                const gesture = this.detectGesture(landmarks);
                if (gesture) {
                    this.handleGesture(gesture);
                }
            }
        } else {
            // Draw "no hands detected" message
            this.ctx.fillStyle = '#00ff88';
            this.ctx.font = '14px Courier New';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('🤘 Wave your hands!', 150, 100);
            this.ctx.fillText('Draw gestures to code', 150, 120);
        }
        
        // Show current gesture pattern
        this.drawGestureInfo();
    }
    
    drawHandLandmarks(landmarks, handLabel) {
        // Draw hand connections
        const connections = [
            [0, 1], [1, 2], [2, 3], [3, 4],  // Thumb
            [0, 5], [5, 6], [6, 7], [7, 8],  // Index
            [5, 9], [9, 10], [10, 11], [11, 12],  // Middle
            [9, 13], [13, 14], [14, 15], [15, 16],  // Ring
            [13, 17], [17, 18], [18, 19], [19, 20]   // Pinky
        ];
        
        // Draw connections
        this.ctx.strokeStyle = '#00ff88';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        
        connections.forEach(([start, end]) => {
            const startPoint = landmarks[start];
            const endPoint = landmarks[end];
            
            this.ctx.moveTo(startPoint.x * this.canvasElement.width, 
                           startPoint.y * this.canvasElement.height);
            this.ctx.lineTo(endPoint.x * this.canvasElement.width, 
                          endPoint.y * this.canvasElement.height);
        });
        this.ctx.stroke();
        
        // Draw landmarks
        landmarks.forEach((landmark, index) => {
            const x = landmark.x * this.canvasElement.width;
            const y = landmark.y * this.canvasElement.height;
            
            this.ctx.fillStyle = index === 8 ? '#ff0066' : '#00ff88';  // Highlight index finger tip
            this.ctx.beginPath();
            this.ctx.arc(x, y, 3, 0, 2 * Math.PI);
            this.ctx.fill();
        });
        
        // Show hand label
        this.ctx.fillStyle = '#ffff88';
        this.ctx.font = '12px Courier New';
        this.ctx.fillText(`${handLabel} Hand`, 10, 20);
    }
    
    detectGesture(landmarks) {
        const now = Date.now();
        if (now - this.lastGestureTime < 100) return null;  // Throttle gesture detection
        
        // Get index finger tip position (landmark 8)
        const indexTip = landmarks[8];
        const x = indexTip.x * this.canvasElement.width;
        const y = indexTip.y * this.canvasElement.height;
        
        // Add to gesture buffer
        this.gestureBuffer.push({ x, y, timestamp: now });
        
        // Keep only recent positions (last 2 seconds)
        this.gestureBuffer = this.gestureBuffer.filter(pos => now - pos.timestamp < 2000);
        
        // Analyze gesture pattern
        if (this.gestureBuffer.length > 10) {
            const pattern = this.analyzeGesturePattern();
            if (pattern) {
                this.lastGestureTime = now;
                return pattern;
            }
        }
        
        return null;
    }
    
    analyzeGesturePattern() {
        if (this.gestureBuffer.length < 10) return null;
        
        const movements = [];
        const threshold = 20;  // Minimum movement distance
        
        for (let i = 1; i < this.gestureBuffer.length; i++) {
            const prev = this.gestureBuffer[i - 1];
            const curr = this.gestureBuffer[i];
            
            const dx = curr.x - prev.x;
            const dy = curr.y - prev.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > threshold) {
                if (Math.abs(dx) > Math.abs(dy)) {
                    movements.push(dx > 0 ? 'right' : 'left');
                } else {
                    movements.push(dy > 0 ? 'down' : 'up');
                }
            }
        }
        
        if (movements.length < 3) return null;
        
        const patternString = movements.slice(-5).join('-');  // Last 5 movements
        
        // Check against known patterns
        for (const [gesture, config] of Object.entries(this.gesturePatterns)) {
            if (patternString.includes(config.pattern)) {
                return gesture;
            }
        }
        
        // Special patterns
        if (this.isCircularGesture()) return 'circle-right';
        if (this.isZigzagGesture()) return 'zigzag';
        
        return null;
    }
    
    isCircularGesture() {
        if (this.gestureBuffer.length < 15) return false;
        
        const recent = this.gestureBuffer.slice(-15);
        let directionChanges = 0;
        let lastDirection = null;
        
        for (let i = 1; i < recent.length; i++) {
            const dx = recent[i].x - recent[i-1].x;
            const dy = recent[i].y - recent[i-1].y;
            
            const angle = Math.atan2(dy, dx);
            const direction = Math.round(angle / (Math.PI / 4));  // Quantize to 8 directions
            
            if (lastDirection !== null && direction !== lastDirection) {
                directionChanges++;
            }
            lastDirection = direction;
        }
        
        return directionChanges > 6;  // Circular motion has many direction changes
    }
    
    isZigzagGesture() {
        if (this.gestureBuffer.length < 10) return false;
        
        const recent = this.gestureBuffer.slice(-10);
        let directionChanges = 0;
        let lastDx = 0;
        
        for (let i = 1; i < recent.length; i++) {
            const dx = recent[i].x - recent[i-1].x;
            
            if (Math.abs(dx) > 10 && Math.sign(dx) !== Math.sign(lastDx) && lastDx !== 0) {
                directionChanges++;
            }
            if (Math.abs(dx) > 10) lastDx = dx;
        }
        
        return directionChanges >= 3;
    }
    
    handleGesture(gestureType) {
        const pattern = this.gesturePatterns[gestureType];
        if (!pattern) return;
        
        console.log(`🤘 Gesture detected: ${gestureType} - ${pattern.description}`);
        
        // Add gesture to history
        this.gestureHistory.push({
            type: gestureType,
            timestamp: Date.now(),
            description: pattern.description
        });
        
        // Keep only last 5 gestures
        this.gestureHistory = this.gestureHistory.slice(-5);
        
        // Apply code to editor
        this.applyGestureCode(pattern.code, pattern.description);
        
        // Visual feedback
        this.showGestureFeedback(pattern.description);
        
        // Clear gesture buffer
        this.gestureBuffer = [];
    }
    
    applyGestureCode(code, description) {
        const codeInput = document.getElementById('codeInput');
        if (!codeInput) return;
        
        if (code === '') {
            // Clear code
            codeInput.value = '';
        } else {
            // Add code with newlines
            const currentCode = codeInput.value;
            const separator = currentCode && !currentCode.endsWith('\n') ? '\n\n' : '';
            codeInput.value = currentCode + separator + code + '\n';
        }
        
        // Trigger change event for any listeners
        codeInput.dispatchEvent(new Event('input', { bubbles: true }));
        
        // Show notification in the UI
        this.showCodeNotification(`🤘 ${description} added via gesture!`);
    }
    
    showGestureFeedback(description) {
        // Create floating feedback element
        const feedback = document.createElement('div');
        feedback.style.position = 'fixed';
        feedback.style.top = '50%';
        feedback.style.left = '50%';
        feedback.style.transform = 'translate(-50%, -50%)';
        feedback.style.background = 'rgba(0, 255, 136, 0.9)';
        feedback.style.color = '#000';
        feedback.style.padding = '20px 40px';
        feedback.style.borderRadius = '15px';
        feedback.style.fontSize = '24px';
        feedback.style.fontWeight = 'bold';
        feedback.style.fontFamily = 'Courier New, monospace';
        feedback.style.zIndex = '10000';
        feedback.style.boxShadow = '0 0 30px rgba(0, 255, 136, 0.6)';
        feedback.style.animation = 'gesturePopup 2s ease-out forwards';
        feedback.textContent = description;
        
        // Add animation CSS
        if (!document.getElementById('gesture-animations')) {
            const style = document.createElement('style');
            style.id = 'gesture-animations';
            style.textContent = `
                @keyframes gesturePopup {
                    0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
                    20% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
                    80% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                    100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(feedback);
        
        // Remove after animation
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.parentNode.removeChild(feedback);
            }
        }, 2000);
    }
    
    showCodeNotification(message) {
        console.log(`📢 ${message}`);
        // Could integrate with existing notification system
        if (window.showNotification) {
            window.showNotification(message);
        }
    }
    
    drawGestureInfo() {
        // Draw gesture patterns help
        this.ctx.fillStyle = '#ffff88';
        this.ctx.font = '10px Courier New';
        this.ctx.textAlign = 'left';
        
        let y = this.canvasElement.height - 60;
        this.ctx.fillText('Gestures:', 10, y);
        y += 12;
        this.ctx.fillText('↓→↓ = Function', 10, y);
        y += 10;
        this.ctx.fillText('↑→↓ = If Statement', 10, y);
        y += 10;
        this.ctx.fillText('○ = Crypto Imports', 10, y);
        y += 10;
        this.ctx.fillText('⚡ = Security Scan', 10, y);
    }
    
    toggle() {
        if (!this.isEnabled) {
            console.log('❌ AR Gestures not available');
            return false;
        }
        
        this.isTracking = !this.isTracking;
        this.canvasElement.style.display = this.isTracking ? 'block' : 'none';
        
        console.log(`🤘 AR Gestures ${this.isTracking ? 'enabled' : 'disabled'}`);
        return this.isTracking;
    }
    
    getGestureHistory() {
        return this.gestureHistory;
    }
}

// Export for use
window.ARGestureCodeInput = ARGestureCodeInput;