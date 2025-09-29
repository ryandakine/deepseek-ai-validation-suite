/**
 * 🎤 VOICE COMMAND INTEGRATION - DEEPSEEK AI VALIDATION
 * "Alexa, validate this crypto code" level shit
 * Speech recognition for completely hands-free validation
 * #ResendMCPHackathon #VoiceControl #GODTIER #NextLevel
 */

class VoiceCommandSystem {
    constructor() {
        this.isListening = false;
        this.recognition = null;
        this.isSupported = false;
        this.lastCommand = null;
        this.commandHistory = [];
        
        // Voice command patterns
        this.commands = {
            // Validation commands
            'validate': {
                patterns: [
                    /validate this code/i,
                    /run validation/i,
                    /check this code/i,
                    /analyze this/i
                ],
                action: 'validate',
                description: '🔍 Start code validation'
            },
            'validate_crypto': {
                patterns: [
                    /validate.*crypto/i,
                    /crypto.*audit/i,
                    /check.*cryptocurrency/i,
                    /analyze.*bitcoin/i
                ],
                action: 'validate_crypto',
                description: '🏦 Validate cryptocurrency code'
            },
            'validate_betting': {
                patterns: [
                    /validate.*betting/i,
                    /check.*gambling/i,
                    /kelly.*criterion/i,
                    /betting.*algorithm/i
                ],
                action: 'validate_betting',
                description: '🎲 Validate betting algorithm'
            },
            'validate_security': {
                patterns: [
                    /validate.*security/i,
                    /security.*scan/i,
                    /penetration.*test/i,
                    /hack.*check/i
                ],
                action: 'validate_security',
                description: '🔒 Validate security code'
            },
            
            // Email commands
            'email_report': {
                patterns: [
                    /email.*report/i,
                    /send.*email/i,
                    /mail.*validation/i,
                    /email.*results/i
                ],
                action: 'email_report',
                description: '📧 Email validation report'
            },
            
            // Interface commands
            'clear_code': {
                patterns: [
                    /clear.*code/i,
                    /delete.*all/i,
                    /start.*over/i,
                    /reset.*editor/i
                ],
                action: 'clear_code',
                description: '🧹 Clear code editor'
            },
            'enable_ar': {
                patterns: [
                    /enable.*gestures/i,
                    /start.*ar/i,
                    /turn.*on.*camera/i,
                    /activate.*gestures/i
                ],
                action: 'enable_ar',
                description: '🤘 Enable AR gestures'
            },
            'disable_ar': {
                patterns: [
                    /disable.*gestures/i,
                    /stop.*ar/i,
                    /turn.*off.*camera/i,
                    /deactivate.*gestures/i
                ],
                action: 'disable_ar',
                description: '🛑 Disable AR gestures'
            },
            
            // Session commands
            'join_session': {
                patterns: [
                    /join.*session/i,
                    /connect.*room/i,
                    /enter.*collaboration/i
                ],
                action: 'join_session',
                description: '🎯 Join collaboration session'
            },
            
            // Unhinged Mode commands
            'enable_unhinged': {
                patterns: [
                    /unhinged.*mode/i,
                    /enable.*unhinged/i,
                    /activate.*unhinged/i,
                    /battle.*mode/i,
                    /llm.*battle/i,
                    /let.*them.*fight/i
                ],
                action: 'enable_unhinged',
                description: '🔥 Activate unhinged LLM battle mode'
            },
            'disable_unhinged': {
                patterns: [
                    /disable.*unhinged/i,
                    /stop.*battle/i,
                    /calm.*down/i,
                    /deactivate.*unhinged/i
                ],
                action: 'disable_unhinged',
                description: '🛄 Deactivate unhinged mode'
            },
            
            // Fun commands for demo
            'demo_mode': {
                patterns: [
                    /demo.*mode/i,
                    /show.*off/i,
                    /impress.*judges/i,
                    /blow.*minds/i
                ],
                action: 'demo_mode',
                description: '🎪 Activate demo mode'
            }
        };
        
        this.demoCommands = [
            "Try saying: 'validate this crypto code'",
            "Try saying: 'email report to judge'",
            "Try saying: 'enable AR gestures'",
            "Try saying: 'activate unhinged mode'",
            "Try saying: 'let them fight'",
            "Try saying: 'clear code'",
            "Try saying: 'demo mode activate'"
        ];
    }
    
    async init() {
        try {
            // Check for speech recognition support
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                console.log('❌ Speech Recognition not supported');
                return false;
            }
            
            // Initialize speech recognition
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            // Event handlers
            this.recognition.onresult = (event) => this.handleSpeechResult(event);
            this.recognition.onerror = (event) => this.handleSpeechError(event);
            this.recognition.onstart = () => this.handleSpeechStart();
            this.recognition.onend = () => this.handleSpeechEnd();
            
            this.isSupported = true;
            console.log('🎤 Voice Commands initialized successfully');
            console.log('📢 Available commands:', Object.keys(this.commands));
            
            return true;
        } catch (error) {
            console.error('❌ Voice Commands failed to initialize:', error);
            return false;
        }
    }
    
    startListening() {
        if (!this.isSupported || this.isListening) return false;
        
        try {
            this.recognition.start();
            console.log('🎤 Voice Commands: Listening...');
            return true;
        } catch (error) {
            console.error('❌ Failed to start listening:', error);
            return false;
        }
    }
    
    stopListening() {
        if (!this.isSupported || !this.isListening) return;
        
        this.recognition.stop();
        console.log('🔇 Voice Commands: Stopped listening');
    }
    
    toggle() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
        return this.isListening;
    }
    
    handleSpeechResult(event) {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Show interim results for feedback
        if (interimTranscript) {
            this.showVoiceTranscript(interimTranscript, false);
        }
        
        // Process final command
        if (finalTranscript) {
            this.showVoiceTranscript(finalTranscript, true);
            this.processCommand(finalTranscript.trim());
        }
    }
    
    handleSpeechError(event) {
        console.error('🎤 Speech recognition error:', event.error);
        
        const errorMessages = {
            'no-speech': 'No speech detected. Try speaking closer to the microphone.',
            'audio-capture': 'Microphone not accessible. Please allow microphone access.',
            'not-allowed': 'Microphone access denied. Please enable microphone permissions.',
            'network': 'Network error occurred during speech recognition.'
        };
        
        const message = errorMessages[event.error] || `Speech recognition error: ${event.error}`;
        this.showVoiceError(message);
    }
    
    handleSpeechStart() {
        this.isListening = true;
        this.updateVoiceUI(true);
        console.log('🎤 Voice recognition started');
    }
    
    handleSpeechEnd() {
        this.isListening = false;
        this.updateVoiceUI(false);
        console.log('🔇 Voice recognition ended');
        
        // Auto-restart if we were intentionally listening
        if (this.shouldKeepListening) {
            setTimeout(() => this.startListening(), 100);
        }
    }
    
    processCommand(transcript) {
        console.log('🎤 Processing voice command:', transcript);
        
        // Find matching command
        let matchedCommand = null;
        let matchedAction = null;
        
        for (const [commandName, commandConfig] of Object.entries(this.commands)) {
            for (const pattern of commandConfig.patterns) {
                if (pattern.test(transcript)) {
                    matchedCommand = commandName;
                    matchedAction = commandConfig.action;
                    break;
                }
            }
            if (matchedCommand) break;
        }
        
        if (matchedCommand) {
            this.executeCommand(matchedAction, transcript);
            this.addToHistory(transcript, matchedCommand);
        } else {
            this.showVoiceUnknownCommand(transcript);
            this.suggestSimilarCommands(transcript);
        }
    }
    
    executeCommand(action, transcript) {
        console.log(`🎤 Executing voice command: ${action}`);
        
        // Show command execution feedback
        this.showVoiceCommandFeedback(action, transcript);
        
        switch (action) {
            case 'validate':
                this.triggerValidation('general_validation');
                break;
                
            case 'validate_crypto':
                this.triggerValidation('crypto_audit');
                break;
                
            case 'validate_betting':
                this.triggerValidation('betting_algorithm');
                break;
                
            case 'validate_security':
                this.triggerValidation('security_testing');
                break;
                
            case 'email_report':
                this.triggerEmailReport();
                break;
                
            case 'clear_code':
                this.clearCodeEditor();
                break;
                
            case 'enable_ar':
                this.toggleAR(true);
                break;
                
            case 'disable_ar':
                this.toggleAR(false);
                break;
                
            case 'join_session':
                this.triggerJoinSession();
                break;
                
            case 'enable_unhinged':
                this.toggleUnhingedMode(true);
                break;
                
            case 'disable_unhinged':
                this.toggleUnhingedMode(false);
                break;
                
            case 'demo_mode':
                this.activateDemoMode();
                break;
                
            default:
                console.log('🤷‍♂️ Unknown action:', action);
        }
    }
    
    triggerValidation(type) {
        const validationTypeSelect = document.getElementById('validationType');
        const validateButton = document.getElementById('validateBtn');
        
        if (validationTypeSelect && validateButton) {
            validationTypeSelect.value = type;
            validateButton.click();
            
            this.speak(`Starting ${type.replace('_', ' ')} validation`);
        }
    }
    
    triggerEmailReport() {
        const emailButton = document.getElementById('emailBtn');
        if (emailButton) {
            emailButton.click();
            this.speak('Sending validation report via email');
        }
    }
    
    clearCodeEditor() {
        const codeInput = document.getElementById('codeInput');
        if (codeInput) {
            codeInput.value = '';
            codeInput.dispatchEvent(new Event('input', { bubbles: true }));
            this.speak('Code editor cleared');
        }
    }
    
    toggleAR(enable) {
        const arButton = document.getElementById('arToggleBtn');
        if (arButton && window.arGestures) {
            if (enable && !window.arGestures.isTracking) {
                arButton.click();
                this.speak('AR gestures enabled');
            } else if (!enable && window.arGestures.isTracking) {
                arButton.click();
                this.speak('AR gestures disabled');
            }
        }
    }
    
    triggerJoinSession() {
        const joinButton = document.getElementById('joinBtn');
        if (joinButton && !joinButton.disabled) {
            joinButton.click();
            this.speak('Joining collaboration session');
        }
    }
    
    activateDemoMode() {
        this.speak('Demo mode activated! Preparing to blow some minds!');
        this.showDemoModeEffects();
    }
    
    toggleUnhingedMode(enable) {
        const unhingedButton = document.getElementById('unhingedBtn');
        if (unhingedButton && window.unhingedMode !== undefined) {
            if (enable && !window.unhingedMode) {
                unhingedButton.click();
                this.speak('Unhinged mode activated! LLMs will now battle each other!');
            } else if (!enable && window.unhingedMode) {
                unhingedButton.click();
                this.speak('Unhinged mode deactivated. LLMs calmed down.');
            } else if (enable === undefined) {
                // Toggle mode
                unhingedButton.click();
                const newState = window.unhingedMode;
                this.speak(newState ? 'Unhinged mode activated!' : 'Unhinged mode deactivated');
            }
        } else {
            this.speak('Unhinged mode controls not available');
        }
    }
    
    
    showDemoModeEffects() {
        // Create dramatic demo mode visual
        const demoOverlay = document.createElement('div');
        demoOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, rgba(255,0,102,0.1), rgba(0,255,136,0.1));
            z-index: 9999;
            pointer-events: none;
            animation: demoModePulse 3s ease-in-out;
        `;
        
        document.body.appendChild(demoOverlay);
        
        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes demoModePulse {
                0%, 100% { opacity: 0; }
                50% { opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        // Remove after animation
        setTimeout(() => {
            if (demoOverlay.parentNode) {
                demoOverlay.parentNode.removeChild(demoOverlay);
            }
        }, 3000);
        
        // Show demo command hints
        this.showDemoHints();
    }
    
    showDemoHints() {
        const hints = document.createElement('div');
        hints.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 20, 40, 0.95);
            border: 2px solid #00ff88;
            border-radius: 15px;
            padding: 30px;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            z-index: 10000;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
        `;
        
        hints.innerHTML = `
            <h3 style="margin-bottom: 20px;">🎤 Voice Commands Ready!</h3>
            ${this.demoCommands.map(cmd => `<p style="margin: 10px 0;">${cmd}</p>`).join('')}
            <p style="margin-top: 20px; font-size: 12px; opacity: 0.8;">
                Click anywhere to dismiss
            </p>
        `;
        
        document.body.appendChild(hints);
        
        hints.addEventListener('click', () => {
            if (hints.parentNode) {
                hints.parentNode.removeChild(hints);
            }
        });
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (hints.parentNode) {
                hints.parentNode.removeChild(hints);
            }
        }, 10000);
    }
    
    speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 0.8;
            speechSynthesis.speak(utterance);
        }
    }
    
    showVoiceTranscript(transcript, isFinal) {
        // Update or create transcript display
        let transcriptElement = document.getElementById('voice-transcript');
        if (!transcriptElement) {
            transcriptElement = document.createElement('div');
            transcriptElement.id = 'voice-transcript';
            transcriptElement.style.cssText = `
                position: fixed;
                bottom: 80px;
                left: 20px;
                background: rgba(0, 255, 136, 0.9);
                color: #000;
                padding: 10px 15px;
                border-radius: 20px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                z-index: 1000;
                transition: all 0.3s ease;
            `;
            document.body.appendChild(transcriptElement);
        }
        
        transcriptElement.textContent = isFinal ? `✅ "${transcript}"` : `🎤 "${transcript}"`;
        transcriptElement.style.opacity = '1';
        
        // Auto-hide after a few seconds for final transcripts
        if (isFinal) {
            setTimeout(() => {
                if (transcriptElement) {
                    transcriptElement.style.opacity = '0';
                    setTimeout(() => {
                        if (transcriptElement.parentNode) {
                            transcriptElement.parentNode.removeChild(transcriptElement);
                        }
                    }, 300);
                }
            }, 3000);
        }
    }
    
    showVoiceCommandFeedback(action, transcript) {
        const command = this.commands[action] || { description: action };
        
        const feedback = document.createElement('div');
        feedback.style.cssText = `
            position: fixed;
            top: 50%;
            right: 20px;
            transform: translateY(-50%);
            background: rgba(0, 255, 136, 0.9);
            color: #000;
            padding: 15px 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            z-index: 10000;
            animation: voiceFeedbackSlide 0.5s ease-out;
        `;
        
        feedback.innerHTML = `
            <div style="font-size: 16px; margin-bottom: 5px;">${command.description}</div>
            <div style="font-size: 12px; opacity: 0.8;">"${transcript}"</div>
        `;
        
        // Add animation
        if (!document.getElementById('voice-feedback-animations')) {
            const style = document.createElement('style');
            style.id = 'voice-feedback-animations';
            style.textContent = `
                @keyframes voiceFeedbackSlide {
                    from { transform: translateY(-50%) translateX(100px); opacity: 0; }
                    to { transform: translateY(-50%) translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.parentNode.removeChild(feedback);
            }
        }, 3000);
    }
    
    showVoiceError(message) {
        console.error('🎤 Voice error:', message);
        
        const error = document.createElement('div');
        error.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 0, 0, 0.9);
            color: #fff;
            padding: 15px 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            z-index: 10000;
        `;
        
        error.textContent = `🎤 ${message}`;
        document.body.appendChild(error);
        
        setTimeout(() => {
            if (error.parentNode) {
                error.parentNode.removeChild(error);
            }
        }, 5000);
    }
    
    showVoiceUnknownCommand(transcript) {
        console.log('🤷‍♂️ Unknown voice command:', transcript);
        
        const unknown = document.createElement('div');
        unknown.style.cssText = `
            position: fixed;
            bottom: 140px;
            left: 20px;
            background: rgba(255, 136, 0, 0.9);
            color: #000;
            padding: 10px 15px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            z-index: 1000;
        `;
        
        unknown.textContent = `🤷‍♂️ Unknown: "${transcript}"`;
        document.body.appendChild(unknown);
        
        setTimeout(() => {
            if (unknown.parentNode) {
                unknown.parentNode.removeChild(unknown);
            }
        }, 4000);
    }
    
    suggestSimilarCommands(transcript) {
        // Simple similarity matching
        const words = transcript.toLowerCase().split(' ');
        const suggestions = [];
        
        for (const [commandName, commandConfig] of Object.entries(this.commands)) {
            const commandWords = commandConfig.description.toLowerCase();
            if (words.some(word => commandWords.includes(word))) {
                suggestions.push(commandConfig.description);
            }
        }
        
        if (suggestions.length > 0) {
            console.log('💡 Suggested commands:', suggestions);
        }
    }
    
    updateVoiceUI(isListening) {
        // Update voice button if it exists
        const voiceButton = document.getElementById('voiceBtn');
        if (voiceButton) {
            voiceButton.textContent = isListening ? '🔇 STOP VOICE' : '🎤 VOICE COMMANDS';
            voiceButton.style.background = isListening ? 
                'linear-gradient(45deg, #ff0066, #ff6600)' : 
                'linear-gradient(45deg, #ff0066, #00ff88)';
        }
        
        // Show listening indicator
        this.showListeningIndicator(isListening);
    }
    
    showListeningIndicator(show) {
        let indicator = document.getElementById('voice-listening-indicator');
        
        if (show && !indicator) {
            indicator = document.createElement('div');
            indicator.id = 'voice-listening-indicator';
            indicator.style.cssText = `
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 0, 102, 0.9);
                color: #fff;
                padding: 8px 16px;
                border-radius: 20px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
                z-index: 1001;
                animation: voicePulse 1.5s infinite;
            `;
            
            indicator.innerHTML = '🎤 LISTENING...';
            
            // Add pulse animation
            if (!document.getElementById('voice-pulse-animation')) {
                const style = document.createElement('style');
                style.id = 'voice-pulse-animation';
                style.textContent = `
                    @keyframes voicePulse {
                        0%, 100% { opacity: 0.7; transform: translateX(-50%) scale(1); }
                        50% { opacity: 1; transform: translateX(-50%) scale(1.05); }
                    }
                `;
                document.head.appendChild(style);
            }
            
            document.body.appendChild(indicator);
        } else if (!show && indicator) {
            indicator.parentNode.removeChild(indicator);
        }
    }
    
    addToHistory(transcript, command) {
        this.commandHistory.push({
            transcript,
            command,
            timestamp: Date.now()
        });
        
        // Keep only last 20 commands
        if (this.commandHistory.length > 20) {
            this.commandHistory = this.commandHistory.slice(-20);
        }
    }
    
    getCommandHistory() {
        return this.commandHistory;
    }
    
    getAvailableCommands() {
        return Object.entries(this.commands).map(([name, config]) => ({
            name,
            description: config.description,
            patterns: config.patterns.map(p => p.source)
        }));
    }
}

// Export for use
window.VoiceCommandSystem = VoiceCommandSystem;