/**
 * Visual Effects System
 * SVG-based animations inspired by the cyberpunk concept art
 */

export class VisualEffectsSystem {
    constructor(container) {
        this.container = container;
        this.activeEffects = new Map();
        this.effectCounter = 0;
        this.init();
    }
    
    init() {
        // Create SVG overlay for effects
        this.svgOverlay = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        this.svgOverlay.setAttribute('width', '100%');
        this.svgOverlay.setAttribute('height', '100%');
        this.svgOverlay.style.position = 'absolute';
        this.svgOverlay.style.top = '0';
        this.svgOverlay.style.left = '0';
        this.svgOverlay.style.pointerEvents = 'none';
        this.svgOverlay.style.zIndex = '1000';
        
        // Add common definitions
        this.createCommonDefs();
        
        this.container.appendChild(this.svgOverlay);
    }
    
    createCommonDefs() {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        
        // Glow filters
        const glowFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
        glowFilter.setAttribute('id', 'glow-effect');
        glowFilter.setAttribute('x', '-50%');
        glowFilter.setAttribute('y', '-50%');
        glowFilter.setAttribute('width', '200%');
        glowFilter.setAttribute('height', '200%');
        
        const feGaussianBlur = document.createElementNS('http://www.w3.org/2000/svg', 'feGaussianBlur');
        feGaussianBlur.setAttribute('stdDeviation', '3');
        feGaussianBlur.setAttribute('result', 'blur');
        
        const feComposite = document.createElementNS('http://www.w3.org/2000/svg', 'feComposite');
        feComposite.setAttribute('in', 'SourceGraphic');
        feComposite.setAttribute('in2', 'blur');
        feComposite.setAttribute('operator', 'over');
        
        glowFilter.appendChild(feGaussianBlur);
        glowFilter.appendChild(feComposite);
        defs.appendChild(glowFilter);
        
        // ICE attack pattern gradients
        const iceGradient = document.createElementNS('http://www.w3.org/2000/svg', 'radialGradient');
        iceGradient.setAttribute('id', 'ice-attack-gradient');
        iceGradient.setAttribute('cx', '50%');
        iceGradient.setAttribute('cy', '50%');
        iceGradient.setAttribute('r', '50%');
        
        const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop1.setAttribute('offset', '0%');
        stop1.setAttribute('stop-color', '#FF00FF');
        stop1.setAttribute('stop-opacity', '0.8');
        
        const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop2.setAttribute('offset', '100%');
        stop2.setAttribute('stop-color', '#8E44AD');
        stop2.setAttribute('stop-opacity', '0');
        
        iceGradient.appendChild(stop1);
        iceGradient.appendChild(stop2);
        defs.appendChild(iceGradient);
        
        this.svgOverlay.appendChild(defs);
    }
    
    // ICE manifestation effect based on BLACK ICE concept art
    createBlackICEEffect(x, y, options = {}) {
        const effectId = `black-ice-${this.effectCounter++}`;
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.setAttribute('id', effectId);
        group.setAttribute('transform', `translate(${x}, ${y})`);
        
        // Core sphere
        const core = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        core.setAttribute('cx', '0');
        core.setAttribute('cy', '0');
        core.setAttribute('r', '15');
        core.setAttribute('fill', '#FF00FF');
        core.setAttribute('fill-opacity', '0.8');
        core.setAttribute('filter', 'url(#glow-effect)');
        
        // Animate core pulsing
        const coreAnimate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        coreAnimate.setAttribute('attributeName', 'r');
        coreAnimate.setAttribute('values', '12;18;12');
        coreAnimate.setAttribute('dur', '2s');
        coreAnimate.setAttribute('repeatCount', 'indefinite');
        core.appendChild(coreAnimate);
        
        group.appendChild(core);
        
        // Defensive spikes
        const spikeData = [
            { angle: 0, length: 30 },
            { angle: 45, length: 25 },
            { angle: 90, length: 30 },
            { angle: 135, length: 25 },
            { angle: 180, length: 30 },
            { angle: 225, length: 25 },
            { angle: 270, length: 30 },
            { angle: 315, length: 25 }
        ];
        
        spikeData.forEach((spike, index) => {
            const radian = (spike.angle * Math.PI) / 180;
            const x1 = Math.cos(radian) * 15;
            const y1 = Math.sin(radian) * 15;
            const x2 = Math.cos(radian) * (15 + spike.length);
            const y2 = Math.sin(radian) * (15 + spike.length);
            
            const spikeLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            spikeLine.setAttribute('x1', x1);
            spikeLine.setAttribute('y1', y1);
            spikeLine.setAttribute('x2', x2);
            spikeLine.setAttribute('y2', y2);
            spikeLine.setAttribute('stroke', '#FF00FF');
            spikeLine.setAttribute('stroke-width', '3');
            spikeLine.setAttribute('stroke-opacity', '0.9');
            
            // Animate spike extension
            const spikeAnimate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
            spikeAnimate.setAttribute('attributeName', 'x2');
            spikeAnimate.setAttribute('values', `${x1};${x2};${x1}`);
            spikeAnimate.setAttribute('dur', `${2 + index * 0.1}s`);
            spikeAnimate.setAttribute('repeatCount', 'indefinite');
            spikeLine.appendChild(spikeAnimate);
            
            const spikeAnimate2 = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
            spikeAnimate2.setAttribute('attributeName', 'y2');
            spikeAnimate2.setAttribute('values', `${y1};${y2};${y1}`);
            spikeAnimate2.setAttribute('dur', `${2 + index * 0.1}s`);
            spikeAnimate2.setAttribute('repeatCount', 'indefinite');
            spikeLine.appendChild(spikeAnimate2);
            
            group.appendChild(spikeLine);
        });
        
        // Neural damage warning
        const warningText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        warningText.setAttribute('x', '0');
        warningText.setAttribute('y', '-60');
        warningText.setAttribute('text-anchor', 'middle');
        warningText.setAttribute('font-family', 'monospace');
        warningText.setAttribute('font-size', '12');
        warningText.setAttribute('fill', '#FF0000');
        warningText.textContent = 'NEURAL DAMAGE IMMINENT';
        
        const textBlink = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        textBlink.setAttribute('attributeName', 'opacity');
        textBlink.setAttribute('values', '1;0;1');
        textBlink.setAttribute('dur', '1s');
        textBlink.setAttribute('repeatCount', 'indefinite');
        warningText.appendChild(textBlink);
        
        group.appendChild(warningText);
        
        this.svgOverlay.appendChild(group);
        this.activeEffects.set(effectId, group);
        
        // Auto-remove after duration
        if (options.duration) {
            setTimeout(() => this.removeEffect(effectId), options.duration);
        }
        
        return effectId;
    }
    
    // Corporate grid pattern based on cyberspace concept art
    createCorporateGridEffect(options = {}) {
        const effectId = `corp-grid-${this.effectCounter++}`;
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.setAttribute('id', effectId);
        group.setAttribute('opacity', '0.3');
        
        const containerRect = this.container.getBoundingClientRect();
        const width = containerRect.width;
        const height = containerRect.height;
        
        // Perspective grid lines
        const gridSpacing = 50;
        
        // Vertical lines with perspective
        for (let x = 0; x < width; x += gridSpacing) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x);
            line.setAttribute('y1', '0');
            line.setAttribute('x2', x + (x - width/2) * 0.2); // Perspective effect
            line.setAttribute('y2', height);
            line.setAttribute('stroke', '#808080');
            line.setAttribute('stroke-width', '0.5');
            line.setAttribute('stroke-opacity', '0.2');
            group.appendChild(line);
        }
        
        // Horizontal lines
        for (let y = 0; y < height; y += gridSpacing) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', '0');
            line.setAttribute('y1', y);
            line.setAttribute('x2', width);
            line.setAttribute('y2', y);
            line.setAttribute('stroke', '#808080');
            line.setAttribute('stroke-width', '0.5');
            line.setAttribute('stroke-opacity', '0.2');
            group.appendChild(line);
        }
        
        // Add animated data streams
        for (let i = 0; i < 5; i++) {
            const streamPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            const startX = Math.random() * width;
            const startY = Math.random() * height;
            const endX = Math.random() * width;
            const endY = Math.random() * height;
            
            streamPath.setAttribute('d', `M ${startX},${startY} Q ${(startX + endX)/2},${startY - 50} ${endX},${endY}`);
            streamPath.setAttribute('stroke', '#9980FA');
            streamPath.setAttribute('stroke-width', '2');
            streamPath.setAttribute('fill', 'none');
            streamPath.setAttribute('stroke-dasharray', '10 5');
            streamPath.setAttribute('stroke-opacity', '0.6');
            
            const streamAnimate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
            streamAnimate.setAttribute('attributeName', 'stroke-dashoffset');
            streamAnimate.setAttribute('values', '0;30;0');
            streamAnimate.setAttribute('dur', `${3 + Math.random() * 2}s`);
            streamAnimate.setAttribute('repeatCount', 'indefinite');
            streamPath.appendChild(streamAnimate);
            
            group.appendChild(streamPath);
        }
        
        this.svgOverlay.appendChild(group);
        this.activeEffects.set(effectId, group);
        
        if (options.duration) {
            setTimeout(() => this.removeEffect(effectId), options.duration);
        }
        
        return effectId;
    }
    
    // Node junction interface based on concept art
    createNodeJunctionEffect(x, y, connections = [], options = {}) {
        const effectId = `node-junction-${this.effectCounter++}`;
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.setAttribute('id', effectId);
        group.setAttribute('transform', `translate(${x}, ${y})`);
        
        // Central hub
        const hub = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        hub.setAttribute('cx', '0');
        hub.setAttribute('cy', '0');
        hub.setAttribute('r', '30');
        hub.setAttribute('fill', 'none');
        hub.setAttribute('stroke', '#9980FA');
        hub.setAttribute('stroke-width', '3');
        hub.setAttribute('filter', 'url(#glow-effect)');
        
        // Pulse animation
        const hubPulse = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        hubPulse.setAttribute('attributeName', 'r');
        hubPulse.setAttribute('values', '25;35;25');
        hubPulse.setAttribute('dur', '3s');
        hubPulse.setAttribute('repeatCount', 'indefinite');
        hub.appendChild(hubPulse);
        
        group.appendChild(hub);
        
        // Inner core
        const core = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        core.setAttribute('cx', '0');
        core.setAttribute('cy', '0');
        core.setAttribute('r', '10');
        core.setAttribute('fill', '#9980FA');
        core.setAttribute('fill-opacity', '0.6');
        group.appendChild(core);
        
        // Connection pathways
        const pathAngles = [0, 90, 180, 270]; // Four main directions
        pathAngles.forEach((angle, index) => {
            if (connections[index] !== false) {
                const radian = (angle * Math.PI) / 180;
                const startX = Math.cos(radian) * 35;
                const startY = Math.sin(radian) * 35;
                const endX = Math.cos(radian) * 100;
                const endY = Math.sin(radian) * 100;
                
                const pathway = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                pathway.setAttribute('x1', startX);
                pathway.setAttribute('y1', startY);
                pathway.setAttribute('x2', endX);
                pathway.setAttribute('y2', endY);
                pathway.setAttribute('stroke', '#9980FA');
                pathway.setAttribute('stroke-width', '3');
                pathway.setAttribute('stroke-opacity', '0.8');
                
                group.appendChild(pathway);
                
                // Data packet animation
                const packet = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                packet.setAttribute('cx', endX);
                packet.setAttribute('cy', endY);
                packet.setAttribute('r', '3');
                packet.setAttribute('fill', '#9980FA');
                
                const packetMove = document.createElementNS('http://www.w3.org/2000/svg', 'animateTransform');
                packetMove.setAttribute('attributeName', 'transform');
                packetMove.setAttribute('type', 'translate');
                packetMove.setAttribute('values', `${endX} ${endY}; ${startX} ${startY}; ${endX} ${endY}`);
                packetMove.setAttribute('dur', `${4 + index}s`);
                packetMove.setAttribute('repeatCount', 'indefinite');
                packet.appendChild(packetMove);
                
                group.appendChild(packet);
            }
        });
        
        this.svgOverlay.appendChild(group);
        this.activeEffects.set(effectId, group);
        
        if (options.duration) {
            setTimeout(() => this.removeEffect(effectId), options.duration);
        }
        
        return effectId;
    }
    
    // Glitch effect for system corruption
    createGlitchEffect(target, options = {}) {
        const effectId = `glitch-${this.effectCounter++}`;
        const originalElement = target;
        
        // Create glitch overlay
        const glitchOverlay = document.createElement('div');
        glitchOverlay.style.position = 'absolute';
        glitchOverlay.style.top = '0';
        glitchOverlay.style.left = '0';
        glitchOverlay.style.width = '100%';
        glitchOverlay.style.height = '100%';
        glitchOverlay.style.pointerEvents = 'none';
        glitchOverlay.style.zIndex = '999';
        
        // CSS for glitch effect
        const style = document.createElement('style');
        style.textContent = `
            .glitch-${effectId} {
                animation: glitch-${effectId} 0.3s infinite;
            }
            
            @keyframes glitch-${effectId} {
                0% { 
                    transform: translate(0px, 0px);
                    filter: hue-rotate(0deg);
                }
                10% { 
                    transform: translate(-2px, 1px);
                    filter: hue-rotate(90deg);
                }
                20% { 
                    transform: translate(1px, -1px);
                    filter: hue-rotate(180deg);
                }
                30% { 
                    transform: translate(-1px, 2px);
                    filter: hue-rotate(270deg);
                }
                40% { 
                    transform: translate(2px, -2px);
                    filter: hue-rotate(360deg);
                }
                50% { 
                    transform: translate(-2px, 1px) skew(2deg);
                    filter: hue-rotate(45deg) contrast(150%);
                }
                60% { 
                    transform: translate(1px, -1px) skew(-2deg);
                    filter: hue-rotate(135deg) brightness(150%);
                }
                70% { 
                    transform: translate(-1px, 2px);
                    filter: hue-rotate(225deg) saturate(150%);
                }
                80% { 
                    transform: translate(2px, -2px);
                    filter: hue-rotate(315deg);
                }
                90% { 
                    transform: translate(0px, 1px);
                    filter: hue-rotate(0deg);
                }
                100% { 
                    transform: translate(0px, 0px);
                    filter: hue-rotate(0deg);
                }
            }
        `;
        document.head.appendChild(style);
        
        originalElement.classList.add(`glitch-${effectId}`);
        
        this.activeEffects.set(effectId, {
            element: originalElement,
            className: `glitch-${effectId}`,
            style: style
        });
        
        // Auto-remove after duration
        const duration = options.duration || 3000;
        setTimeout(() => this.removeEffect(effectId), duration);
        
        return effectId;
    }
    
    // Screen tear effect for neural damage
    createScreenTearEffect(options = {}) {
        const effectId = `screen-tear-${this.effectCounter++}`;
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.pointerEvents = 'none';
        overlay.style.zIndex = '9999';
        overlay.style.background = `
            linear-gradient(
                90deg,
                transparent 0%,
                rgba(255, 0, 0, 0.1) 25%,
                transparent 50%,
                rgba(0, 255, 0, 0.1) 75%,
                transparent 100%
            )
        `;
        overlay.style.animation = 'screen-tear 0.1s infinite';
        
        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes screen-tear {
                0% { 
                    transform: translateX(0px) scaleX(1);
                    opacity: 0.3;
                }
                25% { 
                    transform: translateX(-10px) scaleX(1.1);
                    opacity: 0.8;
                }
                50% { 
                    transform: translateX(5px) scaleX(0.9);
                    opacity: 0.5;
                }
                75% { 
                    transform: translateX(-5px) scaleX(1.05);
                    opacity: 0.7;
                }
                100% { 
                    transform: translateX(0px) scaleX(1);
                    opacity: 0.3;
                }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(overlay);
        
        this.activeEffects.set(effectId, {
            element: overlay,
            style: style
        });
        
        // Auto-remove
        const duration = options.duration || 2000;
        setTimeout(() => this.removeEffect(effectId), duration);
        
        return effectId;
    }
    
    // Data stream visualization
    createDataStreamEffect(fromX, fromY, toX, toY, options = {}) {
        const effectId = `data-stream-${this.effectCounter++}`;
        
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const midX = (fromX + toX) / 2;
        const midY = (fromY + toY) / 2 - 30; // Slight curve
        
        path.setAttribute('d', `M ${fromX},${fromY} Q ${midX},${midY} ${toX},${toY}`);
        path.setAttribute('stroke', options.color || '#00FF41');
        path.setAttribute('stroke-width', options.width || '2');
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke-dasharray', '8 4');
        path.setAttribute('filter', 'url(#glow-effect)');
        
        const streamAnimate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        streamAnimate.setAttribute('attributeName', 'stroke-dashoffset');
        streamAnimate.setAttribute('from', '0');
        streamAnimate.setAttribute('to', '24');
        streamAnimate.setAttribute('dur', options.speed || '1s');
        streamAnimate.setAttribute('repeatCount', 'indefinite');
        path.appendChild(streamAnimate);
        
        this.svgOverlay.appendChild(path);
        this.activeEffects.set(effectId, path);
        
        if (options.duration) {
            setTimeout(() => this.removeEffect(effectId), options.duration);
        }
        
        return effectId;
    }
    
    // Remove an effect
    removeEffect(effectId) {
        const effect = this.activeEffects.get(effectId);
        if (effect) {
            if (effect.element && effect.className) {
                // Glitch effect cleanup
                effect.element.classList.remove(effect.className);
                if (effect.style) {
                    effect.style.remove();
                }
                if (effect.element.parentNode) {
                    effect.element.parentNode.removeChild(effect.element);
                }
            } else if (effect.parentNode) {
                // SVG effect cleanup
                effect.parentNode.removeChild(effect);
            }
            this.activeEffects.delete(effectId);
        }
    }
    
    // Clear all effects
    clearAllEffects() {
        this.activeEffects.forEach((effect, effectId) => {
            this.removeEffect(effectId);
        });
    }
    
    // Preset combinations
    createICEAttackSequence(x, y) {
        const iceEffect = this.createBlackICEEffect(x, y, { duration: 5000 });
        
        setTimeout(() => {
            this.createGlitchEffect(this.container, { duration: 1000 });
        }, 2000);
        
        setTimeout(() => {
            this.createScreenTearEffect({ duration: 1500 });
        }, 3000);
        
        return [iceEffect];
    }
    
    createNetworkInfiltrationSequence() {
        const gridEffect = this.createCorporateGridEffect({ duration: 10000 });
        
        setTimeout(() => {
            const centerX = this.container.offsetWidth / 2;
            const centerY = this.container.offsetHeight / 2;
            this.createNodeJunctionEffect(centerX, centerY, [true, true, true, true], { duration: 8000 });
        }, 1000);
        
        return [gridEffect];
    }
}