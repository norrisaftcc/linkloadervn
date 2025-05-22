/**
 * Cyberspace Runner Minigame
 * Interactive node navigation inspired by the concept art
 */

export class CyberspaceRunner {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            width: 800,
            height: 500,
            nodeCount: 12,
            pathComplexity: 'medium',
            iceLevel: 'low',
            timeLimit: 60,
            ...options
        };
        
        this.gameState = {
            currentNode: null,
            targetNode: null,
            visitedNodes: new Set(),
            playerPath: [],
            timeRemaining: this.options.timeLimit,
            score: 0,
            iceEncounters: 0,
            gameOver: false,
            success: false
        };
        
        this.nodes = [];
        this.connections = [];
        this.activeICE = [];
        this.gameTimer = null;
        
        this.init();
    }
    
    init() {
        this.createGameArea();
        this.generateCyberscape();
        this.setupEventListeners();
        this.startGame();
    }
    
    createGameArea() {
        this.container.innerHTML = `
            <div class="cyberspace-runner">
                <div class="runner-hud">
                    <div class="hud-left">
                        <div class="time-display">TIME: <span id="time-remaining">${this.options.timeLimit}</span></div>
                        <div class="score-display">SCORE: <span id="score">0</span></div>
                    </div>
                    <div class="hud-center">
                        <div class="objective">NAVIGATE TO TARGET NODE</div>
                    </div>
                    <div class="hud-right">
                        <div class="ice-counter">ICE: <span id="ice-count">0</span></div>
                        <div class="nodes-counter">NODES: <span id="nodes-visited">0</span>/<span id="total-nodes">${this.options.nodeCount}</span></div>
                    </div>
                </div>
                <div class="cyberspace-grid" id="cyberspace-grid">
                    <svg width="${this.options.width}" height="${this.options.height}" id="cyberspace-svg">
                        <defs>
                            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                                <feGaussianBlur stdDeviation="3" result="blur"/>
                                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
                            </filter>
                            <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#9980FA" stop-opacity="0.3"/>
                                <stop offset="100%" stop-color="#00FF41" stop-opacity="0.8"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <div class="runner-controls">
                    <button id="scan-button" class="runner-btn">SCAN</button>
                    <button id="stealth-button" class="runner-btn">STEALTH</button>
                    <button id="boost-button" class="runner-btn">BOOST</button>
                </div>
                <div class="runner-messages" id="runner-messages"></div>
            </div>
        `;
        
        // Add CSS styles
        const style = document.createElement('style');
        style.textContent = `
            .cyberspace-runner {
                width: 100%;
                height: 100vh;
                background: linear-gradient(45deg, #0A0A12, #000000);
                color: #00FF41;
                font-family: 'Courier New', monospace;
                position: relative;
                overflow: hidden;
            }
            
            .runner-hud {
                display: flex;
                justify-content: space-between;
                padding: 10px 20px;
                background: rgba(0, 0, 0, 0.8);
                border-bottom: 1px solid #00FF41;
            }
            
            .cyberspace-grid {
                width: 100%;
                height: calc(100vh - 120px);
                position: relative;
                overflow: hidden;
            }
            
            .runner-controls {
                position: absolute;
                bottom: 60px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
            }
            
            .runner-btn {
                background: rgba(0, 255, 65, 0.2);
                border: 1px solid #00FF41;
                color: #00FF41;
                padding: 8px 16px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .runner-btn:hover {
                background: rgba(0, 255, 65, 0.4);
                box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            }
            
            .runner-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .runner-messages {
                position: absolute;
                bottom: 10px;
                left: 20px;
                right: 20px;
                height: 40px;
                background: rgba(0, 0, 0, 0.8);
                border: 1px solid #00FF41;
                padding: 10px;
                font-size: 12px;
                overflow-y: auto;
            }
            
            .node {
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .node.current {
                filter: url(#glow);
            }
            
            .node.target {
                animation: pulse 2s infinite;
            }
            
            .node.visited {
                opacity: 0.6;
            }
            
            .ice-warning {
                animation: danger-pulse 1s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 0.8; }
                50% { opacity: 1; }
            }
            
            @keyframes danger-pulse {
                0%, 100% { stroke: #FF0000; }
                50% { stroke: #FF8800; }
            }
            
            .connection {
                stroke-dasharray: 5 3;
                animation: data-flow 2s linear infinite;
            }
            
            @keyframes data-flow {
                0% { stroke-dashoffset: 0; }
                100% { stroke-dashoffset: 20; }
            }
        `;
        document.head.appendChild(style);
    }
    
    generateCyberscape() {
        const svg = document.getElementById('cyberspace-svg');
        const width = this.options.width;
        const height = this.options.height;
        
        // Generate nodes in a grid pattern with some randomization
        const cols = Math.ceil(Math.sqrt(this.options.nodeCount));
        const rows = Math.ceil(this.options.nodeCount / cols);
        const colSpacing = width / (cols + 1);
        const rowSpacing = height / (rows + 1);
        
        for (let i = 0; i < this.options.nodeCount; i++) {
            const col = i % cols;
            const row = Math.floor(i / cols);
            
            // Add some randomization to avoid perfect grid
            const randomX = (Math.random() - 0.5) * colSpacing * 0.3;
            const randomY = (Math.random() - 0.5) * rowSpacing * 0.3;
            
            const x = colSpacing * (col + 1) + randomX;
            const y = rowSpacing * (row + 1) + randomY;
            
            const nodeType = this.determineNodeType(i);
            const node = {
                id: `node_${i}`,
                x: x,
                y: y,
                type: nodeType,
                connections: [],
                hasICE: Math.random() < 0.3, // 30% chance of ICE
                iceType: this.randomICEType(),
                visited: false,
                accessible: i === 0 // Only starting node is initially accessible
            };
            
            this.nodes.push(node);
        }
        
        // Set start and target nodes
        this.gameState.currentNode = this.nodes[0];
        this.gameState.targetNode = this.nodes[this.nodes.length - 1];
        
        // Generate connections between nearby nodes
        this.generateConnections();
        
        // Render the cyberscape
        this.renderNodes(svg);
        this.renderConnections(svg);
    }
    
    determineNodeType(index) {
        if (index === 0) return 'start';
        if (index === this.nodes.length - 1) return 'target';
        
        const types = ['database', 'security', 'junction', 'utility', 'corporate'];
        return types[Math.floor(Math.random() * types.length)];
    }
    
    randomICEType() {
        const types = ['SENTRY_ICE', 'BLACK_ICE', 'PHANTOM_ICE', 'BLOODHOUND_ICE'];
        return types[Math.floor(Math.random() * types.length)];
    }
    
    generateConnections() {
        for (let i = 0; i < this.nodes.length; i++) {
            const node = this.nodes[i];
            
            // Connect to nearby nodes
            for (let j = i + 1; j < this.nodes.length; j++) {
                const otherNode = this.nodes[j];
                const distance = Math.sqrt(
                    Math.pow(node.x - otherNode.x, 2) + 
                    Math.pow(node.y - otherNode.y, 2)
                );
                
                // Connect if within reasonable distance
                if (distance < 150 && Math.random() < 0.7) {
                    node.connections.push(j);
                    otherNode.connections.push(i);
                    
                    this.connections.push({
                        from: i,
                        to: j,
                        fromNode: node,
                        toNode: otherNode,
                        secure: Math.random() < 0.2 // 20% chance of secure connection
                    });
                }
            }
        }
        
        // Ensure all nodes are reachable
        this.ensureConnectivity();
    }
    
    ensureConnectivity() {
        const visited = new Set();
        const queue = [0]; // Start from first node
        visited.add(0);
        
        while (queue.length > 0) {
            const nodeIndex = queue.shift();
            const node = this.nodes[nodeIndex];
            
            for (const connectedIndex of node.connections) {
                if (!visited.has(connectedIndex)) {
                    visited.add(connectedIndex);
                    queue.push(connectedIndex);
                }
            }
        }
        
        // Connect any unreachable nodes
        for (let i = 0; i < this.nodes.length; i++) {
            if (!visited.has(i)) {
                // Find nearest reachable node and connect
                let nearestDistance = Infinity;
                let nearestNode = -1;
                
                for (const reachableIndex of visited) {
                    const distance = Math.sqrt(
                        Math.pow(this.nodes[i].x - this.nodes[reachableIndex].x, 2) + 
                        Math.pow(this.nodes[i].y - this.nodes[reachableIndex].y, 2)
                    );
                    
                    if (distance < nearestDistance) {
                        nearestDistance = distance;
                        nearestNode = reachableIndex;
                    }
                }
                
                if (nearestNode !== -1) {
                    this.nodes[i].connections.push(nearestNode);
                    this.nodes[nearestNode].connections.push(i);
                    this.connections.push({
                        from: i,
                        to: nearestNode,
                        fromNode: this.nodes[i],
                        toNode: this.nodes[nearestNode],
                        secure: false
                    });
                    visited.add(i);
                }
            }
        }
    }
    
    renderNodes(svg) {
        this.nodes.forEach((node, index) => {
            const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            group.setAttribute('class', `node ${index === 0 ? 'current' : ''} ${index === this.nodes.length - 1 ? 'target' : ''}`);
            group.setAttribute('data-node-index', index);
            
            // Node circle
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', node.x);
            circle.setAttribute('cy', node.y);
            circle.setAttribute('r', index === 0 || index === this.nodes.length - 1 ? 15 : 10);
            
            // Color based on type
            const colors = {
                start: '#00FF41',
                target: '#FF0080',
                database: '#0984E3',
                security: '#FF0000',
                junction: '#9980FA',
                utility: '#FFFA65',
                corporate: '#FF8800'
            };
            
            circle.setAttribute('fill', colors[node.type] || '#808080');
            circle.setAttribute('stroke', '#FFFFFF');
            circle.setAttribute('stroke-width', '1');
            circle.setAttribute('fill-opacity', '0.7');
            
            // ICE warning indicator
            if (node.hasICE) {
                const warning = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                warning.setAttribute('cx', node.x);
                warning.setAttribute('cy', node.y);
                warning.setAttribute('r', 18);
                warning.setAttribute('fill', 'none');
                warning.setAttribute('stroke', '#FF0000');
                warning.setAttribute('stroke-width', '2');
                warning.setAttribute('class', 'ice-warning');
                group.appendChild(warning);
            }
            
            group.appendChild(circle);
            
            // Node label
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', node.x);
            text.setAttribute('y', node.y + 25);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('font-family', 'Courier New');
            text.setAttribute('font-size', '8');
            text.setAttribute('fill', '#FFFFFF');
            text.textContent = node.type.toUpperCase();
            group.appendChild(text);
            
            // Click handler
            group.addEventListener('click', () => this.attemptMoveToNode(index));
            
            svg.appendChild(group);
        });
    }
    
    renderConnections(svg) {
        this.connections.forEach(connection => {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', connection.fromNode.x);
            line.setAttribute('y1', connection.fromNode.y);
            line.setAttribute('x2', connection.toNode.x);
            line.setAttribute('y2', connection.toNode.y);
            line.setAttribute('stroke', connection.secure ? '#FF8800' : 'url(#pathGradient)');
            line.setAttribute('stroke-width', connection.secure ? '3' : '2');
            line.setAttribute('stroke-opacity', '0.6');
            line.setAttribute('class', 'connection');
            
            svg.appendChild(line);
        });
    }
    
    setupEventListeners() {
        // Control buttons
        document.getElementById('scan-button').addEventListener('click', () => this.useScanAbility());
        document.getElementById('stealth-button').addEventListener('click', () => this.useStealthAbility());
        document.getElementById('boost-button').addEventListener('click', () => this.useBoostAbility());
    }
    
    startGame() {
        this.addMessage("JACK IN SUCCESSFUL. NAVIGATE TO TARGET NODE.");
        this.gameState.currentNode.accessible = true;
        this.updateAccessibleNodes();
        
        this.gameTimer = setInterval(() => {
            this.gameState.timeRemaining--;
            document.getElementById('time-remaining').textContent = this.gameState.timeRemaining;
            
            if (this.gameState.timeRemaining <= 0) {
                this.endGame(false, "TIME EXPIRED");
            }
        }, 1000);
    }
    
    attemptMoveToNode(nodeIndex) {
        const targetNode = this.nodes[nodeIndex];
        const currentNodeIndex = this.nodes.indexOf(this.gameState.currentNode);
        
        // Check if node is accessible
        if (!targetNode.accessible) {
            this.addMessage("NODE NOT ACCESSIBLE - NO DIRECT CONNECTION");
            return;
        }
        
        // Check if it's a valid move (connected to current node)
        if (!this.gameState.currentNode.connections.includes(nodeIndex)) {
            this.addMessage("INVALID MOVE - NODES NOT CONNECTED");
            return;
        }
        
        // Handle ICE encounter
        if (targetNode.hasICE && !targetNode.visited) {
            this.handleICEEncounter(targetNode, nodeIndex);
            return;
        }
        
        // Move to node
        this.moveToNode(nodeIndex);
    }
    
    moveToNode(nodeIndex) {
        const currentNodeIndex = this.nodes.indexOf(this.gameState.currentNode);
        
        // Update current node
        this.gameState.currentNode = this.nodes[nodeIndex];
        this.gameState.visitedNodes.add(nodeIndex);
        this.gameState.playerPath.push(nodeIndex);
        this.nodes[nodeIndex].visited = true;
        
        // Update visual state
        document.querySelector(`[data-node-index="${currentNodeIndex}"]`).classList.remove('current');
        document.querySelector(`[data-node-index="${nodeIndex}"]`).classList.add('current', 'visited');
        
        // Update accessible nodes
        this.updateAccessibleNodes();
        
        // Update HUD
        document.getElementById('nodes-visited').textContent = this.gameState.visitedNodes.size;
        this.gameState.score += 10;
        document.getElementById('score').textContent = this.gameState.score;
        
        this.addMessage(`MOVED TO ${this.nodes[nodeIndex].type.toUpperCase()} NODE`);
        
        // Check win condition
        if (nodeIndex === this.nodes.length - 1) {
            this.endGame(true, "TARGET REACHED - EXTRACTION SUCCESSFUL");
        }
    }
    
    updateAccessibleNodes() {
        // Mark all connected nodes as accessible
        this.gameState.currentNode.connections.forEach(connectedIndex => {
            this.nodes[connectedIndex].accessible = true;
        });
    }
    
    handleICEEncounter(node, nodeIndex) {
        this.gameState.iceEncounters++;
        document.getElementById('ice-count').textContent = this.gameState.iceEncounters;
        
        const iceNames = {
            'SENTRY_ICE': 'SENTRY ICE',
            'BLACK_ICE': 'BLACK ICE', 
            'PHANTOM_ICE': 'PHANTOM ICE',
            'BLOODHOUND_ICE': 'BLOODHOUND ICE'
        };
        
        const iceName = iceNames[node.iceType] || 'UNKNOWN ICE';
        this.addMessage(`${iceName} DETECTED - INITIATING COUNTERMEASURES`);
        
        // Simple ICE combat resolution
        const playerSkill = Math.random() * 10 + 5; // 5-15
        const iceStrength = Math.random() * 8 + 3; // 3-11
        
        if (playerSkill > iceStrength) {
            this.addMessage(`${iceName} DEFEATED - NODE SECURED`);
            node.hasICE = false;
            // Remove visual ICE warning
            const nodeElement = document.querySelector(`[data-node-index="${nodeIndex}"]`);
            const warning = nodeElement.querySelector('.ice-warning');
            if (warning) warning.remove();
            
            this.gameState.score += 25;
            document.getElementById('score').textContent = this.gameState.score;
            this.moveToNode(nodeIndex);
        } else {
            this.addMessage(`${iceName} REPELLED INTRUSION - TAKING DAMAGE`);
            this.gameState.timeRemaining -= 5; // Penalty for failed ICE encounter
            document.getElementById('time-remaining').textContent = this.gameState.timeRemaining;
        }
    }
    
    useScanAbility() {
        // Reveal all ICE in connected nodes
        this.gameState.currentNode.connections.forEach(connectedIndex => {
            const node = this.nodes[connectedIndex];
            if (node.hasICE) {
                this.addMessage(`SCAN: ICE DETECTED IN ${node.type.toUpperCase()} NODE`);
            }
        });
        
        this.addMessage("SCAN COMPLETE - ICE SIGNATURES REVEALED");
        document.getElementById('scan-button').disabled = true;
    }
    
    useStealthAbility() {
        // Next ICE encounter automatically succeeds
        this.stealthActive = true;
        this.addMessage("STEALTH PROTOCOLS ACTIVE - NEXT ICE WILL BE BYPASSED");
        document.getElementById('stealth-button').disabled = true;
    }
    
    useBoostAbility() {
        // Double score for next 3 moves
        this.boostActive = 3;
        this.addMessage("PERFORMANCE BOOST ACTIVE - DOUBLE SCORE FOR 3 MOVES");
        document.getElementById('boost-button').disabled = true;
    }
    
    addMessage(text) {
        const messages = document.getElementById('runner-messages');
        messages.textContent = text;
        // Auto-scroll effect could be added here
    }
    
    endGame(success, message) {
        this.gameState.gameOver = true;
        this.gameState.success = success;
        
        if (this.gameTimer) {
            clearInterval(this.gameTimer);
        }
        
        this.addMessage(message);
        
        // Disable all controls
        document.getElementById('scan-button').disabled = true;
        document.getElementById('stealth-button').disabled = true;
        document.getElementById('boost-button').disabled = true;
        
        // Could trigger callback to parent story here
        if (this.options.onGameEnd) {
            setTimeout(() => {
                this.options.onGameEnd({
                    success: success,
                    score: this.gameState.score,
                    timeRemaining: this.gameState.timeRemaining,
                    nodesVisited: this.gameState.visitedNodes.size,
                    iceEncounters: this.gameState.iceEncounters
                });
            }, 2000);
        }
    }
    
    // Public interface for story integration
    getGameState() {
        return { ...this.gameState };
    }
    
    destroy() {
        if (this.gameTimer) {
            clearInterval(this.gameTimer);
        }
        this.container.innerHTML = '';
    }
}