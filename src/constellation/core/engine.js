/**
 * Constellation Engine - Core Engine Class
 * A web-native visual novel engine for LinkLoader
 */

export class ConstellationEngine {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? 
            document.querySelector(container) : container;
        
        this.options = {
            autoSave: true,
            typewriterSpeed: 50,
            fadeTransitions: true,
            ...options
        };
        
        this.currentScene = null;
        this.gameState = {
            currentSceneId: null,
            variables: {},
            history: [],
            saves: []
        };
        
        this.story = null;
        this.renderer = null;
        this.audioManager = null;
        this.saveManager = null;
        
        this.init();
    }
    
    init() {
        // Initialize the engine container
        this.container.className = 'constellation-engine';
        this.container.innerHTML = `
            <div class="constellation-viewport">
                <div class="constellation-background"></div>
                <div class="constellation-characters"></div>
                <div class="constellation-dialogue-box"></div>
                <div class="constellation-choices"></div>
                <div class="constellation-ui"></div>
            </div>
        `;
        
        this.viewport = this.container.querySelector('.constellation-viewport');
        this.backgroundLayer = this.container.querySelector('.constellation-background');
        this.charactersLayer = this.container.querySelector('.constellation-characters');
        this.dialogueBox = this.container.querySelector('.constellation-dialogue-box');
        this.choicesContainer = this.container.querySelector('.constellation-choices');
        this.uiLayer = this.container.querySelector('.constellation-ui');
        
        console.log('Constellation Engine initialized');
    }
    
    async loadStory(storyData) {
        this.story = storyData;
        console.log(`Loaded story: ${storyData.title}`);
        
        // Start from the first scene or a specified starting point
        const startScene = storyData.startScene || Object.keys(storyData.scenes)[0];
        await this.goToScene(startScene);
    }
    
    async goToScene(sceneId) {
        const scene = this.story.scenes[sceneId];
        if (!scene) {
            console.error(`Scene not found: ${sceneId}`);
            return;
        }
        
        this.currentScene = scene;
        this.gameState.currentSceneId = sceneId;
        
        // Update background
        if (scene.background) {
            this.setBackground(scene.background);
        }
        
        // Update characters
        if (scene.characters) {
            this.setCharacters(scene.characters);
        }
        
        // Start dialogue sequence
        if (scene.dialogue && scene.dialogue.length > 0) {
            await this.playDialogue(scene.dialogue);
        }
        
        // Show choices if available
        if (scene.choices && scene.choices.length > 0) {
            this.showChoices(scene.choices);
        }
        
        console.log(`Entered scene: ${sceneId}`);
    }
    
    setBackground(backgroundImage) {
        this.backgroundLayer.style.backgroundImage = `url(${backgroundImage})`;
        this.backgroundLayer.style.backgroundSize = 'cover';
        this.backgroundLayer.style.backgroundPosition = 'center';
    }
    
    setCharacters(characters) {
        this.charactersLayer.innerHTML = '';
        characters.forEach(char => {
            const charElement = document.createElement('div');
            charElement.className = `character character-${char.name}`;
            charElement.style.backgroundImage = `url(${char.sprite})`;
            charElement.style.backgroundSize = 'contain';
            charElement.style.backgroundRepeat = 'no-repeat';
            charElement.style.backgroundPosition = 'bottom center';
            
            // Position the character
            if (char.position === 'left') charElement.style.left = '10%';
            else if (char.position === 'center') charElement.style.left = '50%';
            else if (char.position === 'right') charElement.style.right = '10%';
            
            this.charactersLayer.appendChild(charElement);
        });
    }
    
    async playDialogue(dialogueLines) {
        for (const line of dialogueLines) {
            await this.showDialogueLine(line);
            await this.waitForUserInput();
        }
    }
    
    async showDialogueLine(line) {
        const speakerName = line.speaker || '';
        const text = line.text || '';
        
        this.dialogueBox.innerHTML = `
            <div class="dialogue-speaker">${speakerName}</div>
            <div class="dialogue-text"></div>
            <div class="dialogue-continue">▼</div>
        `;
        
        const textElement = this.dialogueBox.querySelector('.dialogue-text');
        
        // Typewriter effect
        if (this.options.typewriterSpeed > 0) {
            await this.typewriterEffect(textElement, text);
        } else {
            textElement.textContent = text;
        }
    }
    
    async typewriterEffect(element, text) {
        element.textContent = '';
        for (let i = 0; i < text.length; i++) {
            element.textContent += text[i];
            await this.sleep(this.options.typewriterSpeed);
        }
    }
    
    showChoices(choices) {
        this.choicesContainer.innerHTML = '';
        choices.forEach((choice, index) => {
            const choiceButton = document.createElement('button');
            choiceButton.className = 'choice-button';
            choiceButton.textContent = choice.text;
            choiceButton.onclick = () => this.selectChoice(choice);
            this.choicesContainer.appendChild(choiceButton);
        });
    }
    
    async selectChoice(choice) {
        this.choicesContainer.innerHTML = '';
        
        // Execute choice action
        if (choice.goto) {
            await this.goToScene(choice.goto);
        }
        
        // Handle variable changes
        if (choice.set) {
            Object.assign(this.gameState.variables, choice.set);
        }
    }
    
    waitForUserInput() {
        return new Promise(resolve => {
            const handleClick = () => {
                document.removeEventListener('click', handleClick);
                document.removeEventListener('keydown', handleKeydown);
                resolve();
            };
            
            const handleKeydown = (e) => {
                if (e.key === ' ' || e.key === 'Enter') {
                    handleClick();
                }
            };
            
            document.addEventListener('click', handleClick);
            document.addEventListener('keydown', handleKeydown);
        });
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // Utility methods for game state management
    getVariable(name) {
        return this.gameState.variables[name];
    }
    
    setVariable(name, value) {
        this.gameState.variables[name] = value;
    }
}