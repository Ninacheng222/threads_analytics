// Alpine.js data and interactions
document.addEventListener('alpine:init', () => {
    Alpine.data('dashboard', () => ({
        posts: [],
        selectedPosts: [],
        sortBy: 'engagement_rate',
        sortDesc: true,
        loading: false,
        analytics: {},
        chartType: 'engagement',
        
        async init() {
            await this.loadData();
            this.initChart();
        },
        
        async loadData() {
            this.loading = true;
            try {
                const [postsRes, analyticsRes] = await Promise.all([
                    fetch('/api/posts'),
                    fetch('/api/analytics')
                ]);
                
                this.posts = await postsRes.json();
                this.analytics = await analyticsRes.json();
                this.sortPosts();
            } catch (error) {
                console.error('Error loading data:', error);
            }
            this.loading = false;
        },
        
        async syncData() {
            this.loading = true;
            try {
                await fetch('/api/sync', { method: 'POST' });
                await this.loadData();
            } catch (error) {
                console.error('Error syncing data:', error);
            }
            this.loading = false;
        },
        
        sortPosts() {
            this.posts.sort((a, b) => {
                const aVal = a[this.sortBy];
                const bVal = b[this.sortBy];
                return this.sortDesc ? bVal - aVal : aVal - bVal;
            });
        },
        
        sortBy(column) {
            if (this.sortBy === column) {
                this.sortDesc = !this.sortDesc;
            } else {
                this.sortBy = column;
                this.sortDesc = true;
            }
            this.sortPosts();
        },
        
        togglePost(postId) {
            const index = this.selectedPosts.indexOf(postId);
            if (index > -1) {
                this.selectedPosts.splice(index, 1);
            } else {
                this.selectedPosts.push(postId);
            }
        },
        
        toggleAllPosts() {
            if (this.selectedPosts.length === this.posts.length) {
                this.selectedPosts = [];
            } else {
                this.selectedPosts = this.posts.map(p => p.thread_id);
            }
        },
        
        async analyzeSelected() {
            if (this.selectedPosts.length === 0) return;
            
            this.loading = true;
            try {
                await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ post_ids: this.selectedPosts })
                });
                await this.loadData();
                this.selectedPosts = [];
            } catch (error) {
                console.error('Error analyzing posts:', error);
            }
            this.loading = false;
        },
        
        getEngagementClass(rate) {
            if (rate > 5) return 'engagement-high';
            if (rate > 2) return 'engagement-medium';
            return 'engagement-low';
        },
        
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString();
        },
        
        truncateText(text, length = 100) {
            return text.length > length ? text.substring(0, length) + '...' : text;
        },
        
        switchChart(type) {
            this.chartType = type;
            this.updateChart();
        },
        
        initChart() {
            const ctx = document.getElementById('performanceChart').getContext('2d');
            this.chart = new Chart(ctx, {
                type: 'line',
                data: this.getChartData(),
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Post Performance Over Time'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },
        
        getChartData() {
            const sortedPosts = [...this.posts].sort((a, b) => 
                new Date(a.created_at) - new Date(b.created_at)
            );
            
            return {
                labels: sortedPosts.map(p => this.formatDate(p.created_at)),
                datasets: [{
                    label: this.chartType === 'engagement' ? 'Engagement Rate (%)' : 
                           this.chartType === 'views' ? 'Views' : 'Likes',
                    data: sortedPosts.map(p => p[this.chartType === 'engagement' ? 'engagement_rate' : this.chartType]),
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4
                }]
            };
        },
        
        updateChart() {
            this.chart.data = this.getChartData();
            this.chart.update();
        }
    }));
});