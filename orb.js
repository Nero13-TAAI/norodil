// Animated Orb Effect for Hero Section
class AnimatedOrb {
    constructor(container) {
        this.container = container;
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.container.appendChild(this.canvas);

        this.time = 0;
        this.mouseX = 0.5;
        this.mouseY = 0.5;
        this.targetMouseX = 0.5;
        this.targetMouseY = 0.5;

        this.resize();
        this.setupEventListeners();
        this.animate();
    }

    resize() {
        const dpr = window.devicePixelRatio || 1;
        const rect = this.container.getBoundingClientRect();
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
        this.ctx.scale(dpr, dpr);
        this.width = rect.width;
        this.height = rect.height;
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.resize());

        this.container.addEventListener('mousemove', (e) => {
            const rect = this.container.getBoundingClientRect();
            this.targetMouseX = (e.clientX - rect.left) / rect.width;
            this.targetMouseY = (e.clientY - rect.top) / rect.height;
        });

        this.container.addEventListener('mouseleave', () => {
            this.targetMouseX = 0.5;
            this.targetMouseY = 0.5;
        });
    }

    drawGradientOrb(x, y, radius, hue) {
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, radius);

        // Gold-based color scheme
        const color1 = `hsla(${hue}, 70%, 60%, 0.8)`;
        const color2 = `hsla(${hue + 20}, 60%, 50%, 0.5)`;
        const color3 = `hsla(${hue - 20}, 50%, 40%, 0.2)`;
        const color4 = `hsla(${hue}, 40%, 30%, 0)`;

        gradient.addColorStop(0, color1);
        gradient.addColorStop(0.3, color2);
        gradient.addColorStop(0.6, color3);
        gradient.addColorStop(1, color4);

        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, Math.PI * 2);
        this.ctx.fill();
    }

    animate() {
        this.time += 0.01;

        // Smooth mouse follow
        this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
        this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;

        // Clear canvas
        this.ctx.clearRect(0, 0, this.width, this.height);

        const centerX = this.width / 2;
        const centerY = this.height / 2;
        const baseRadius = Math.min(this.width, this.height) * 0.4;

        // Main orb with pulsing effect
        const pulse = Math.sin(this.time * 2) * 0.1 + 1;
        const mainRadius = baseRadius * pulse;
        const offsetX = (this.mouseX - 0.5) * 50;
        const offsetY = (this.mouseY - 0.5) * 50;

        // Gold hue (45 degrees)
        const goldHue = 45;

        // Draw multiple layers for depth
        this.ctx.globalCompositeOperation = 'screen';

        // Layer 1: Outer glow
        this.drawGradientOrb(
            centerX + offsetX * 0.5,
            centerY + offsetY * 0.5,
            mainRadius * 1.5,
            goldHue + Math.sin(this.time) * 10
        );

        // Layer 2: Main orb
        this.drawGradientOrb(
            centerX + offsetX,
            centerY + offsetY,
            mainRadius,
            goldHue
        );

        // Layer 3: Rotating inner orb
        const angle = this.time * 0.5;
        const innerX = centerX + offsetX + Math.cos(angle) * 50;
        const innerY = centerY + offsetY + Math.sin(angle) * 50;
        this.drawGradientOrb(
            innerX,
            innerY,
            mainRadius * 0.6,
            goldHue + 30
        );

        // Layer 4: Counter-rotating accent
        const angle2 = -this.time * 0.7;
        const accentX = centerX + offsetX + Math.cos(angle2) * 70;
        const accentY = centerY + offsetY + Math.sin(angle2) * 70;
        this.drawGradientOrb(
            accentX,
            accentY,
            mainRadius * 0.4,
            goldHue - 20
        );

        // Add noise/sparkle effect
        this.ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < 20; i++) {
            const sparkleAngle = this.time * 2 + i * 0.3;
            const sparkleRadius = mainRadius * 0.8 + Math.sin(this.time * 3 + i) * 20;
            const sparkleX = centerX + offsetX + Math.cos(sparkleAngle) * sparkleRadius;
            const sparkleY = centerY + offsetY + Math.sin(sparkleAngle) * sparkleRadius;
            const sparkleSize = Math.sin(this.time * 5 + i) * 2 + 2;

            this.ctx.fillStyle = `rgba(255, 215, 0, ${Math.sin(this.time * 4 + i) * 0.3 + 0.3})`;
            this.ctx.beginPath();
            this.ctx.arc(sparkleX, sparkleY, sparkleSize, 0, Math.PI * 2);
            this.ctx.fill();
        }

        requestAnimationFrame(() => this.animate());
    }
}

// Initialize orb when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const orbContainer = document.getElementById('orb-container');
    if (orbContainer) {
        new AnimatedOrb(orbContainer);
    }
});
