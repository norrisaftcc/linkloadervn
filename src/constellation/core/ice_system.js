/**
 * ICE (Intrusion Countermeasures Electronics) System
 * Based on concept art designs - different ICE types with unique behaviors
 */

export class ICESystem {
    constructor() {
        this.activeICE = new Map();
        this.iceTypes = this.initializeICETypes();
    }
    
    initializeICETypes() {
        return {
            // Based on black-ice-svg.svg - Lethal neural feedback system
            BLACK_ICE: {
                name: "BLACK ICE",
                description: "Lethal defensive system with neural feedback capabilities",
                manufacturer: "MAAS-NEOTEK",
                version: "v3.7",
                stats: {
                    attack: 8,
                    defense: 6,
                    speed: 4,
                    detectability: 9
                },
                abilities: [
                    "neural_damage",
                    "adaptive_defense", 
                    "spike_barrage",
                    "system_corruption"
                ],
                weakness: "logic_bombs",
                behavior: "aggressive_hunter",
                visualEffects: {
                    idle: "pulsing_sphere_with_spikes",
                    attacking: "extending_neural_spikes",
                    damaged: "flickering_core"
                }
            },
            
            // Based on sentry-ice-svg.svg - Scanning and tracking system
            SENTRY_ICE: {
                name: "SENTRY ICE", 
                description: "Methodical scanning system with geometric precision",
                manufacturer: "ARASAKA",
                version: "v2.1",
                stats: {
                    attack: 4,
                    defense: 8,
                    speed: 6,
                    detectability: 7
                },
                abilities: [
                    "deep_scan",
                    "alarm_trigger",
                    "backup_summon",
                    "trace_initiation"
                ],
                weakness: "stealth_programs",
                behavior: "methodical_patrol",
                visualEffects: {
                    idle: "geometric_scanning_pattern",
                    scanning: "blue_sweep_beams", 
                    alert: "red_geometric_expansion"
                }
            },
            
            // Based on bloodhound-ice-svg.svg - Tracking and pursuit
            BLOODHOUND_ICE: {
                name: "BLOODHOUND ICE",
                description: "Persistent tracking system that follows data trails",
                manufacturer: "MILITECH",
                version: "v4.2",
                stats: {
                    attack: 6,
                    defense: 4,
                    speed: 9,
                    detectability: 5
                },
                abilities: [
                    "data_trail_tracking",
                    "persistent_pursuit",
                    "pack_coordination",
                    "stealth_detection"
                ],
                weakness: "signal_scramblers",
                behavior: "relentless_hunter",
                visualEffects: {
                    idle: "prowling_energy_form",
                    tracking: "following_data_streams",
                    pursuit: "rapid_geometric_chase"
                }
            },
            
            // Based on phantom-ice-svg.svg - Deceptive and elusive
            PHANTOM_ICE: {
                name: "PHANTOM ICE",
                description: "Deceptive system that creates false data and illusions",
                manufacturer: "ZETATECH",
                version: "v1.8",
                stats: {
                    attack: 5,
                    defense: 3,
                    speed: 8,
                    detectability: 2
                },
                abilities: [
                    "false_data_injection",
                    "illusion_creation",
                    "phase_shifting",
                    "reality_distortion"
                ],
                weakness: "authentication_protocols",
                behavior: "deceptive_mirage",
                visualEffects: {
                    idle: "shimmering_translucent_form",
                    deceiving: "multiple_false_copies",
                    phasing: "transparency_fluctuation"
                }
            },
            
            // Based on sphinx-ice-svg.svg - Puzzle and riddle system
            SPHINX_ICE: {
                name: "SPHINX ICE",
                description: "Enigmatic system that challenges intruders with puzzles",
                manufacturer: "BIOTECHNICA",
                version: "v3.0",
                stats: {
                    attack: 3,
                    defense: 9,
                    speed: 2,
                    detectability: 8
                },
                abilities: [
                    "logic_puzzles",
                    "riddle_challenges",
                    "temporal_loops",
                    "wisdom_testing"
                ],
                weakness: "brute_force_attacks",
                behavior: "guardian_challenger",
                visualEffects: {
                    idle: "ancient_geometric_patterns",
                    challenging: "holographic_puzzles",
                    defeated: "crumbling_stone_effect"
                }
            },
            
            // Based on wall-ice-svg.svg - Barrier and blocking system
            WALL_ICE: {
                name: "WALL ICE",
                description: "Massive barrier system designed to block all intrusion",
                manufacturer: "KANG TAO",
                version: "v5.1",
                stats: {
                    attack: 1,
                    defense: 10,
                    speed: 1,
                    detectability: 10
                },
                abilities: [
                    "impenetrable_barrier",
                    "structural_reinforcement",
                    "damage_absorption",
                    "fortress_mode"
                ],
                weakness: "bypass_protocols",
                behavior: "immovable_guardian",
                visualEffects: {
                    idle: "massive_geometric_wall",
                    reinforcing: "crystalline_growth",
                    breached: "structural_collapse"
                }
            }
        };
    }
    
    // Spawn ICE based on security level and corporate faction
    spawnICE(securityLevel, corporateFaction, quantity = 1) {
        const icePool = this.getAvailableICE(securityLevel, corporateFaction);
        const spawnedICE = [];
        
        for (let i = 0; i < quantity; i++) {
            const iceType = this.selectRandomICE(icePool);
            const iceInstance = this.createICEInstance(iceType);
            spawnedICE.push(iceInstance);
            this.activeICE.set(iceInstance.id, iceInstance);
        }
        
        return spawnedICE;
    }
    
    getAvailableICE(securityLevel, faction) {
        const allICE = Object.keys(this.iceTypes);
        
        // Filter by security level
        let availableICE = allICE.filter(iceType => {
            const ice = this.iceTypes[iceType];
            if (securityLevel === 'low') return ice.stats.attack <= 4;
            if (securityLevel === 'medium') return ice.stats.attack <= 6;
            if (securityLevel === 'high') return ice.stats.attack <= 8;
            if (securityLevel === 'maximum') return true;
            return false;
        });
        
        // Faction preferences
        const factionPreferences = {
            'ARASAKA': ['SENTRY_ICE', 'BLACK_ICE'],
            'MILITECH': ['BLOODHOUND_ICE', 'WALL_ICE'],
            'BIOTECHNICA': ['SPHINX_ICE', 'PHANTOM_ICE'],
            'MAAS_NEOTEK': ['BLACK_ICE', 'WALL_ICE'],
            'ZETATECH': ['PHANTOM_ICE', 'SENTRY_ICE']
        };
        
        if (factionPreferences[faction]) {
            // Weight faction-preferred ICE more heavily
            const preferred = factionPreferences[faction].filter(ice => availableICE.includes(ice));
            const others = availableICE.filter(ice => !factionPreferences[faction].includes(ice));
            availableICE = [...preferred, ...preferred, ...others]; // Double weight for preferred
        }
        
        return availableICE;
    }
    
    selectRandomICE(icePool) {
        return icePool[Math.floor(Math.random() * icePool.length)];
    }
    
    createICEInstance(iceType) {
        const baseICE = this.iceTypes[iceType];
        return {
            id: `ice_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type: iceType,
            name: baseICE.name,
            description: baseICE.description,
            manufacturer: baseICE.manufacturer,
            version: baseICE.version,
            stats: { ...baseICE.stats },
            abilities: [...baseICE.abilities],
            weakness: baseICE.weakness,
            behavior: baseICE.behavior,
            visualEffects: { ...baseICE.visualEffects },
            currentHealth: baseICE.stats.defense,
            maxHealth: baseICE.stats.defense,
            status: 'idle', // idle, scanning, attacking, damaged, destroyed
            lastAction: null,
            target: null
        };
    }
    
    // Combat resolution system
    combatRound(attackerProgram, targetICE) {
        const ice = this.activeICE.get(targetICE.id);
        if (!ice) return { success: false, message: "ICE not found" };
        
        // Calculate attack effectiveness
        let attackPower = attackerProgram.power || 5;
        let defense = ice.stats.defense;
        
        // Check for weakness exploitation
        if (attackerProgram.type === ice.weakness) {
            attackPower *= 2;
        }
        
        // Apply random variance
        const variance = 0.2;
        const randomFactor = 1 + (Math.random() - 0.5) * variance;
        attackPower *= randomFactor;
        
        const damage = Math.max(0, attackPower - defense);
        ice.currentHealth -= damage;
        
        // Determine ICE response
        let response = this.generateICEResponse(ice, damage);
        
        if (ice.currentHealth <= 0) {
            ice.status = 'destroyed';
            this.activeICE.delete(ice.id);
            response.iceDestroyed = true;
        } else if (damage > 0) {
            ice.status = 'damaged';
        }
        
        return {
            success: true,
            damage: Math.round(damage * 10) / 10,
            iceHealth: ice.currentHealth,
            iceMaxHealth: ice.maxHealth,
            iceResponse: response
        };
    }
    
    generateICEResponse(ice, damageReceived) {
        const responses = {
            BLACK_ICE: {
                low_damage: "The BLACK ICE's spikes retract and pulse with malevolent energy.",
                medium_damage: "Neural feedback crackles through the connection as the BLACK ICE adapts.",
                high_damage: "The BLACK ICE shrieks in digital fury, preparing a devastating counterattack.",
                critical: "The BLACK ICE core flickers, but its death throes promise neural devastation."
            },
            SENTRY_ICE: {
                low_damage: "The SENTRY ICE recalibrates its geometric patterns.",
                medium_damage: "Security protocols escalate as the SENTRY ICE calls for backup.",
                high_damage: "The SENTRY ICE's scanning beams intensify, seeking weak points.",
                critical: "Emergency protocols engage as the SENTRY ICE prepares final countermeasures."
            },
            BLOODHOUND_ICE: {
                low_damage: "The BLOODHOUND ICE snarls and begins tracking your signature.",
                medium_damage: "Wounded, the BLOODHOUND ICE becomes more aggressive in its pursuit.",
                high_damage: "The BLOODHOUND ICE howls across the network, calling its pack.",
                critical: "Dying, the BLOODHOUND ICE makes one last desperate lunge."
            },
            PHANTOM_ICE: {
                low_damage: "The PHANTOM ICE flickers and creates false damage indicators.",
                medium_damage: "Reality distorts as the PHANTOM ICE phases between dimensions.",
                high_damage: "The PHANTOM ICE splits into multiple false copies.",
                critical: "The PHANTOM ICE's illusions falter as its true form becomes visible."
            },
            SPHINX_ICE: {
                low_damage: "The SPHINX ICE poses a riddle: 'What thinks it can wound wisdom itself?'",
                medium_damage: "Ancient patterns glow as the SPHINX ICE prepares a logic trap.",
                high_damage: "The SPHINX ICE's voice echoes: 'You show promise, but can you solve THIS?'",
                critical: "The SPHINX ICE crumbles, whispering: 'You have earned passage, clever one.'"
            },
            WALL_ICE: {
                low_damage: "The WALL ICE reinforces itself, growing thicker and more imposing.",
                medium_damage: "Cracks appear in the WALL ICE, but it continues to stand firm.",
                high_damage: "The WALL ICE shudders but activates emergency repair protocols.",
                critical: "The WALL ICE trembles, massive chunks beginning to fall away."
            }
        };
        
        const iceResponses = responses[ice.type] || responses.BLACK_ICE;
        let damageLevel;
        
        const damagePercent = damageReceived / ice.maxHealth;
        if (damagePercent < 0.1) damageLevel = 'low_damage';
        else if (damagePercent < 0.3) damageLevel = 'medium_damage';  
        else if (damagePercent < 0.6) damageLevel = 'high_damage';
        else damageLevel = 'critical';
        
        return {
            message: iceResponses[damageLevel],
            iceType: ice.type,
            behaviorChange: this.determineBehaviorChange(ice, damageLevel),
            counterAttack: this.generateCounterAttack(ice, damageLevel)
        };
    }
    
    determineBehaviorChange(ice, damageLevel) {
        const changes = {
            'low_damage': { aggressiveness: 1.1, speed: 1.0 },
            'medium_damage': { aggressiveness: 1.3, speed: 1.1 },
            'high_damage': { aggressiveness: 1.5, speed: 1.2 },
            'critical': { aggressiveness: 2.0, speed: 0.8 }
        };
        
        return changes[damageLevel] || changes['low_damage'];
    }
    
    generateCounterAttack(ice, damageLevel) {
        if (damageLevel === 'low_damage' && Math.random() < 0.3) return null;
        if (damageLevel === 'medium_damage' && Math.random() < 0.7) return null;
        
        const attacks = {
            BLACK_ICE: [
                { type: 'neural_spike', damage: 6, message: "Neural spikes lance through your connection!" },
                { type: 'system_corruption', damage: 4, message: "Your programs begin to corrupt and malfunction!" },
                { type: 'feedback_loop', damage: 8, message: "Biofeedback overload threatens your nervous system!" }
            ],
            SENTRY_ICE: [
                { type: 'precision_beam', damage: 4, message: "A focused scanning beam disrupts your systems!" },
                { type: 'alert_cascade', damage: 2, message: "Security alerts flood the network!" },
                { type: 'trace_lock', damage: 3, message: "The ICE locks onto your location!" }
            ],
            BLOODHOUND_ICE: [
                { type: 'pack_attack', damage: 5, message: "The BLOODHOUND calls its pack - multiple ICE converge!" },
                { type: 'data_maul', damage: 7, message: "Digital claws tear through your defensive programs!" },
                { type: 'persistent_track', damage: 3, message: "The BLOODHOUND marks you for continuous pursuit!" }
            ],
            PHANTOM_ICE: [
                { type: 'false_reality', damage: 3, message: "Reality distorts - you can't tell what's real!" },
                { type: 'phase_attack', damage: 5, message: "The PHANTOM attacks from an impossible angle!" },
                { type: 'illusion_trap', damage: 4, message: "You're caught in a maze of false data!" }
            ],
            SPHINX_ICE: [
                { type: 'logic_bomb', damage: 6, message: "A complex riddle overloads your reasoning circuits!" },
                { type: 'paradox_loop', damage: 5, message: "An unsolvable paradox traps your processing power!" },
                { type: 'wisdom_drain', damage: 4, message: "The SPHINX draws power from your knowledge!" }
            ],
            WALL_ICE: [
                { type: 'crushing_weight', damage: 8, message: "The massive barrier attempts to crush you!" },
                { type: 'fortress_mode', damage: 0, message: "The WALL becomes completely impenetrable!" },
                { type: 'structural_slam', damage: 6, message: "Sections of the wall slam together violently!" }
            ]
        };
        
        const iceAttacks = attacks[ice.type] || attacks.BLACK_ICE;
        return iceAttacks[Math.floor(Math.random() * iceAttacks.length)];
    }
    
    // Get all active ICE for display/interaction
    getActiveICE() {
        return Array.from(this.activeICE.values());
    }
    
    // Remove ICE (for story progression)
    removeICE(iceId) {
        return this.activeICE.delete(iceId);
    }
    
    // Clear all ICE (scene transitions)
    clearAllICE() {
        this.activeICE.clear();
    }
}