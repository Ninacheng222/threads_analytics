// Fortune Teller App Logic
document.addEventListener('alpine:init', () => {
    Alpine.data('fortuneTeller', () => ({
        currentStep: 'landing', // landing, connecting, reading, results
        readingStep: 0,
        loading: false,
        portrait: {},
        shareableContent: {},
        
        async init() {
            // Initialize the mystical experience
            console.log('🔮 Mystical energies activated...');
        },
        
        async startReading() {
            this.currentStep = 'connecting';
        },
        
        async connectThreads() {
            this.currentStep = 'reading';
            this.readingStep = 0;
            
            // First sync data from Threads
            await this.syncThreadsData();
            
            // Animate through reading steps
            await this.animateReading();
            
            // Generate the portrait
            await this.generatePortrait();
        },
        
        async syncThreadsData() {
            try {
                const response = await fetch('/api/sync', {
                    method: 'POST'
                });
                
                if (!response.ok) {
                    throw new Error('Failed to sync data');
                }
                
                const result = await response.json();
                console.log('✨ Data synced:', result);
                
            } catch (error) {
                console.error('Sync error:', error);
                // Continue with demo data for MVP
            }
        },
        
        async animateReading() {
            const steps = [1, 2, 3, 4];
            
            for (const step of steps) {
                await new Promise(resolve => setTimeout(resolve, 800));
                this.readingStep = step;
            }
            
            // Extra pause for dramatic effect
            await new Promise(resolve => setTimeout(resolve, 1000));
        },
        
        async generatePortrait() {
            this.loading = true;
            
            try {
                const response = await fetch('/api/generate-portrait', {
                    method: 'POST'
                });
                
                if (!response.ok) {
                    throw new Error('Failed to generate portrait');
                }
                
                const result = await response.json();
                this.portrait = result.portrait;
                this.shareableContent = result.shareable_content;
                
                this.currentStep = 'results';
                
            } catch (error) {
                console.error('Portrait generation error:', error);
                // Use demo data for MVP
                this.portrait = this.getDemoPortrait();
                this.shareableContent = this.getDemoShareableContent();
                this.currentStep = 'results';
            }
            
            this.loading = false;
        },
        
        async shareToThreads() {
            const shareUrl = this.shareableContent.share_urls?.threads;
            if (shareUrl) {
                window.open(shareUrl, '_blank');
            } else {
                // Fallback: copy text to clipboard
                this.copyText();
            }
        },
        
        async shareToInstagram() {
            // For IG Stories, we need to use the Web Share API or provide instructions
            if (navigator.share) {
                try {
                    await navigator.share({
                        title: '🔮 My Creator DNA',
                        text: this.shareableContent.share_urls?.copy_text || 'Check out my mystical creator portrait!',
                        url: window.location.origin
                    });
                } catch (error) {
                    console.log('Share cancelled');
                }
            } else {
                // Fallback: download image or copy text
                this.downloadImage();
            }
        },
        
        async copyText() {
            const text = this.shareableContent.share_urls?.copy_text || this.getDefaultShareText();
            
            try {
                await navigator.clipboard.writeText(text);
                this.showToast('✨ Copied to clipboard!');
            } catch (error) {
                // Fallback for older browsers
                this.fallbackCopyText(text);
            }
        },
        
        downloadImage() {
            // Create download link for the generated image
            const imageData = this.shareableContent.ig_story_image;
            if (imageData) {
                const link = document.createElement('a');
                link.href = imageData;
                link.download = 'my-creator-dna.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                this.showToast('📸 Image downloaded!');
            }
        },
        
        fallbackCopyText(text) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('✨ Copied to clipboard!');
        },
        
        showToast(message) {
            // Simple toast notification
            const toast = document.createElement('div');
            toast.className = 'fixed top-4 right-4 bg-cosmic-purple text-white px-6 py-3 rounded-lg shadow-lg z-50';
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 3000);
        },
        
        retakeReading() {
            this.currentStep = 'landing';
            this.readingStep = 0;
            this.portrait = {};
            this.shareableContent = {};
        },
        
        getDefaultShareText() {
            return `🔮 Just discovered my Creator DNA! ✨

${this.portrait.shareable_quote || '✨ Your creative energy is unique ✨'}

My digital aura reveals:
🎭 Archetype: ${this.portrait.archetype || 'The Emerging Creator'}
🌙 Posting Spirit: ${this.portrait.posting_spirit || 'Digital Wanderer'}

What's YOUR creator personality? 

Find out your mystical creator portrait 👇
threadsfortune.app

#CreatorDNA #ThreadsPersonality #ContentCreator #CreatorQuiz`;
        },
        
        getDemoPortrait() {
            // Demo data for testing
            return {
                archetype: "The Authentic Storyteller",
                content_dna: {
                    personal: 45,
                    educational: 30,
                    entertainment: 25
                },
                posting_spirit: "Night Owl Creator",
                engagement_insight: "Your audience craves your vulnerable authenticity",
                creator_level: "Rising Star ⭐",
                mystical_advice: "The universe rewards consistency over perfection",
                shareable_quote: "✨ Your content resonates with the frequency of authenticity ✨",
                total_posts: 12,
                avg_engagement: 4.2
            };
        },
        
        getDemoShareableContent() {
            return {
                ig_story_image: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                share_urls: {
                    threads: "https://threads.net/intent/post?text=" + encodeURIComponent(this.getDefaultShareText()),
                    copy_text: this.getDefaultShareText()
                }
            };
        }
    }));
});