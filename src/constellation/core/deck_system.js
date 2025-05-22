/**
 * Cyberdeck Customization System
 * Allows players to customize their netrunning equipment and programs
 */

export class CyberdeckSystem {
    constructor() {
        this.deckTypes = this.initializeDeckTypes();
        this.programs = this.initializePrograms();
        this.hardware = this.initializeHardware();
        this.playerDeck = this.createStarterDeck();
    }
    
    initializeDeckTypes() {
        return {
            STREET_SPECIAL: {
                name: "Street Special",
                manufacturer: "Underground",
                price: 5000,
                rarity: "common",
                description: "Cobbled together from spare parts, but it works. Popular among street runners.",
                stats: {
                    processing_power: 3,
                    memory_slots: 4,
                    defense_rating: 2,
                    stealth_modifier: 0,
                    max_programs: 6
                },
                specialAbilities: ["jury_rigging"],
                upgradeSlots: {
                    cpu: 1,
                    memory: 2, 
                    defense: 1,
                    cooling: 1
                }
            },
            
            NEUROMANCER_MK4: {
                name: "Neuromancer MK4",
                manufacturer: "Gibson Cybernetics",
                price: 25000,
                rarity: "rare",
                description: "Professional-grade deck favored by serious netrunners. Reliable and powerful.",
                stats: {
                    processing_power: 6,
                    memory_slots: 8,
                    defense_rating: 5,
                    stealth_modifier: 2,
                    max_programs: 10
                },
                specialAbilities: ["adaptive_protocols", "enhanced_encryption"],
                upgradeSlots: {
                    cpu: 2,
                    memory: 3,
                    defense: 2,
                    cooling: 2
                }
            },
            
            MILITECH_FORTRESS: {
                name: "Militech Fortress",
                manufacturer: "Militech",
                price: 40000,
                rarity: "military",
                description: "Military-grade cyberdeck with emphasis on protection and brute force capability.",
                stats: {
                    processing_power: 8,
                    memory_slots: 6,
                    defense_rating: 9,
                    stealth_modifier: -2,
                    max_programs: 8
                },
                specialAbilities: ["hardened_systems", "military_encryption", "trace_immunity"],
                upgradeSlots: {
                    cpu: 3,
                    memory: 2,
                    defense: 4,
                    cooling: 2
                }
            },
            
            ZETATECH_PHANTOM: {
                name: "ZetaTech Phantom",
                manufacturer: "ZetaTech",
                price: 35000,
                rarity: "corporate",
                description: "Cutting-edge stealth deck designed for covert operations and deep infiltration.",
                stats: {
                    processing_power: 7,
                    memory_slots: 10,
                    defense_rating: 4,
                    stealth_modifier: 6,
                    max_programs: 12
                },
                specialAbilities: ["ghost_protocols", "phase_shifting", "neural_masking"],
                upgradeSlots: {
                    cpu: 2,
                    memory: 4,
                    defense: 1,
                    cooling: 3
                }
            },
            
            ARASAKA_EMPEROR: {
                name: "Arasaka Emperor",
                manufacturer: "Arasaka",
                price: 75000,
                rarity: "legendary",
                description: "Top-of-the-line corporate deck. Expensive, powerful, and nearly impossible to obtain legally.",
                stats: {
                    processing_power: 10,
                    memory_slots: 12,
                    defense_rating: 8,
                    stealth_modifier: 4,
                    max_programs: 15
                },
                specialAbilities: ["executive_access", "neural_dominance", "quantum_encryption", "auto_defense"],
                upgradeSlots: {
                    cpu: 4,
                    memory: 4,
                    defense: 3,
                    cooling: 3
                }
            }
        };
    }
    
    initializePrograms() {
        return {
            // Attack Programs
            ICE_PICK: {
                name: "Ice Pick",
                type: "attack",
                category: "basic_attack",
                version: "2.1",
                size: 1,
                price: 1000,
                description: "Basic ICE breaking utility. Effective against simple barriers.",
                stats: {
                    attack_power: 3,
                    accuracy: 8,
                    stealth: 2,
                    execution_time: 2
                },
                effectiveness: {
                    WALL_ICE: 1.5,
                    SENTRY_ICE: 1.0,
                    BLACK_ICE: 0.7
                },
                requirements: {
                    processing_power: 2,
                    memory_slots: 1
                }
            },
            
            HAMMER: {
                name: "Hammer",
                type: "attack", 
                category: "brute_force",
                version: "4.7",
                size: 2,
                price: 5000,
                description: "Brute force attack program. High damage but easily detected.",
                stats: {
                    attack_power: 8,
                    accuracy: 6,
                    stealth: 1,
                    execution_time: 1
                },
                effectiveness: {
                    WALL_ICE: 2.0,
                    BLACK_ICE: 1.2,
                    PHANTOM_ICE: 0.5
                },
                requirements: {
                    processing_power: 4,
                    memory_slots: 2
                }
            },
            
            SCALPEL: {
                name: "Scalpel",
                type: "attack",
                category: "precision_attack", 
                version: "1.8",
                size: 2,
                price: 8000,
                description: "Surgical precision attack. Lower damage but extremely accurate and stealthy.",
                stats: {
                    attack_power: 5,
                    accuracy: 10,
                    stealth: 9,
                    execution_time: 3
                },
                effectiveness: {
                    SENTRY_ICE: 1.8,
                    SPHINX_ICE: 1.5,
                    PHANTOM_ICE: 1.3
                },
                requirements: {
                    processing_power: 5,
                    memory_slots: 2
                }
            },
            
            // Defense Programs
            BARRIER: {
                name: "Barrier",
                type: "defense",
                category: "basic_defense",
                version: "3.2", 
                size: 1,
                price: 2000,
                description: "Basic defensive program. Provides modest protection against ICE attacks.",
                stats: {
                    defense_bonus: 3,
                    duration: 5,
                    activation_time: 1,
                    stealth_penalty: 0
                },
                requirements: {
                    processing_power: 2,
                    memory_slots: 1
                }
            },
            
            FORTRESS: {
                name: "Fortress",
                type: "defense",
                category: "heavy_defense",
                version: "2.0",
                size: 3,
                price: 12000,
                description: "Heavy defensive suite. Excellent protection but resource intensive.",
                stats: {
                    defense_bonus: 8,
                    duration: 8,
                    activation_time: 2,
                    stealth_penalty: -3
                },
                requirements: {
                    processing_power: 6,
                    memory_slots: 3
                }
            },
            
            // Stealth Programs
            GHOST: {
                name: "Ghost",
                type: "stealth",
                category: "invisibility",
                version: "5.1",
                size: 2,
                price: 10000,
                description: "Advanced stealth program. Makes detection extremely difficult.",
                stats: {
                    stealth_bonus: 7,
                    duration: 10,
                    activation_time: 2,
                    processing_drain: 1
                },
                requirements: {
                    processing_power: 4,
                    memory_slots: 2
                }
            },
            
            SMOKE: {
                name: "Smoke",
                type: "stealth",
                category: "obfuscation",
                version: "1.3",
                size: 1,
                price: 3000,
                description: "Creates false signatures to confuse scanning systems.",
                stats: {
                    stealth_bonus: 4,
                    duration: 6,
                    activation_time: 1,
                    processing_drain: 0
                },
                requirements: {
                    processing_power: 2,
                    memory_slots: 1
                }
            },
            
            // Utility Programs
            SCANNER: {
                name: "Scanner",
                type: "utility",
                category: "reconnaissance",
                version: "7.4",
                size: 1,
                price: 4000,
                description: "Reveals ICE types, network topology, and security levels.",
                stats: {
                    scan_range: 3,
                    detail_level: 8,
                    execution_time: 1,
                    detection_risk: 2
                },
                requirements: {
                    processing_power: 3,
                    memory_slots: 1
                }
            },
            
            MEDIC: {
                name: "Medic",
                type: "utility",
                category: "recovery",
                version: "2.9",
                size: 1,
                price: 6000,
                description: "Repairs neural damage and restores system integrity.",
                stats: {
                    healing_power: 5,
                    execution_time: 2,
                    uses_per_run: 3,
                    side_effects: "none"
                },
                requirements: {
                    processing_power: 3,
                    memory_slots: 1
                }
            },
            
            TRACE_BUSTER: {
                name: "Trace Buster",
                type: "utility", 
                category: "counter_surveillance",
                version: "4.1",
                size: 2,
                price: 8000,
                description: "Breaks trace programs and covers your digital tracks.",
                stats: {
                    trace_break_power: 8,
                    execution_time: 1,
                    success_rate: 85,
                    cooldown: 3
                },
                requirements: {
                    processing_power: 4,
                    memory_slots: 2
                }
            },
            
            // Advanced/Illegal Programs
            VIRUS_BOMB: {
                name: "Virus Bomb",
                type: "attack",
                category: "malware",
                version: "ILLEGAL",
                size: 3,
                price: 25000,
                description: "Devastating malware that can cripple entire systems. Highly illegal.",
                stats: {
                    system_damage: 10,
                    spread_rate: 9,
                    detection_delay: 5,
                    collateral_damage: "high"
                },
                legality: "banned_worldwide",
                consequences: "corporate_retaliation_guaranteed",
                requirements: {
                    processing_power: 8,
                    memory_slots: 3
                }
            },
            
            NEURAL_SPIKE: {
                name: "Neural Spike",
                type: "attack",
                category: "anti_personnel",
                version: "ILLEGAL",
                size: 2,
                price: 20000,
                description: "Targets human operators directly. Can cause permanent neural damage.",
                stats: {
                    neural_damage: 9,
                    trace_difficulty: 10,
                    lethality: "potentially_fatal",
                    moral_weight: "extreme"
                },
                legality: "banned_worldwide",
                consequences: "law_enforcement_attention",
                requirements: {
                    processing_power: 6,
                    memory_slots: 2
                }
            }
        };
    }
    
    initializeHardware() {
        return {
            // CPU Upgrades
            PROCESSOR_BOOST_MK1: {
                name: "Processor Boost MK1",
                type: "cpu",
                manufacturer: "Generic Tech",
                price: 3000,
                description: "Basic processing power upgrade.",
                effect: { processing_power: +2 },
                requirements: { upgrade_slots: 1 }
            },
            
            QUANTUM_CORE: {
                name: "Quantum Processing Core",
                type: "cpu", 
                manufacturer: "Arasaka",
                price: 15000,
                description: "Cutting-edge quantum processor. Massive performance boost.",
                effect: { processing_power: +5, stealth_modifier: +1 },
                requirements: { upgrade_slots: 2 }
            },
            
            // Memory Upgrades
            EXTRA_RAM: {
                name: "Extra RAM Module",
                type: "memory",
                manufacturer: "Multiple",
                price: 2000,
                description: "Additional memory for more programs.",
                effect: { memory_slots: +2 },
                requirements: { upgrade_slots: 1 }
            },
            
            NEURAL_STORAGE: {
                name: "Neural Storage Matrix", 
                type: "memory",
                manufacturer: "ZetaTech",
                price: 12000,
                description: "Bio-neural storage system. Massive capacity.",
                effect: { memory_slots: +4, max_programs: +2 },
                requirements: { upgrade_slots: 2 }
            },
            
            // Defense Upgrades
            FIREWALL_BOOST: {
                name: "Firewall Enhancer",
                type: "defense",
                manufacturer: "Militech",
                price: 5000,
                description: "Strengthens defensive capabilities.",
                effect: { defense_rating: +3 },
                requirements: { upgrade_slots: 1 }
            },
            
            ABLATIVE_ARMOR: {
                name: "Ablative Neural Armor",
                type: "defense",
                manufacturer: "Biotechnica",
                price: 10000,
                description: "Biological neural protection. Absorbs neural damage.",
                effect: { defense_rating: +4, neural_damage_resistance: +5 },
                requirements: { upgrade_slots: 2 }
            },
            
            // Cooling Systems
            HEAT_SINK: {
                name: "Advanced Heat Sink",
                type: "cooling",
                manufacturer: "Kang Tao",
                price: 4000,
                description: "Prevents overheating during intensive operations.",
                effect: { overheating_resistance: +3, sustained_ops: +2 },
                requirements: { upgrade_slots: 1 }
            },
            
            CRYO_COOLING: {
                name: "Cryogenic Cooling System",
                type: "cooling",
                manufacturer: "Arasaka",
                price: 18000,
                description: "Exotic cooling system. Allows extreme overclocking.",
                effect: { overheating_resistance: +8, processing_power: +2, stealth_modifier: +2 },
                requirements: { upgrade_slots: 3 }
            }
        };
    }
    
    createStarterDeck() {
        return {
            base_deck: "STREET_SPECIAL",
            installed_programs: ["ICE_PICK", "BARRIER", "SMOKE", "SCANNER"],
            installed_hardware: [],
            current_stats: { ...this.deckTypes.STREET_SPECIAL.stats },
            used_upgrade_slots: {
                cpu: 0,
                memory: 0,
                defense: 0,
                cooling: 0
            },
            condition: 100, // 0-100, affects performance
            heat_level: 0,   // 0-100, high heat reduces performance
            neural_integrity: 100 // Player's neural health
        };
    }
    
    // Get effective deck stats including all modifications
    getEffectiveDeckStats() {
        const baseDeck = this.deckTypes[this.playerDeck.base_deck];
        let effectiveStats = { ...baseDeck.stats };
        
        // Apply hardware modifications
        this.playerDeck.installed_hardware.forEach(hardwareKey => {
            const hardware = this.hardware[hardwareKey];
            if (hardware && hardware.effect) {
                Object.keys(hardware.effect).forEach(stat => {
                    if (effectiveStats[stat] !== undefined) {
                        effectiveStats[stat] += hardware.effect[stat];
                    } else {
                        effectiveStats[stat] = hardware.effect[stat];
                    }
                });
            }
        });
        
        // Apply condition penalties
        const conditionMultiplier = this.playerDeck.condition / 100;
        effectiveStats.processing_power = Math.floor(effectiveStats.processing_power * conditionMultiplier);
        effectiveStats.defense_rating = Math.floor(effectiveStats.defense_rating * conditionMultiplier);
        
        // Apply heat penalties
        if (this.playerDeck.heat_level > 70) {
            const heatPenalty = Math.floor((this.playerDeck.heat_level - 70) / 10);
            effectiveStats.processing_power = Math.max(1, effectiveStats.processing_power - heatPenalty);
        }
        
        return effectiveStats;
    }
    
    // Install a program
    installProgram(programKey) {
        const program = this.programs[programKey];
        if (!program) return { success: false, message: "Program not found" };
        
        const stats = this.getEffectiveDeckStats();
        
        // Check memory slots
        const currentMemoryUsage = this.calculateMemoryUsage();
        if (currentMemoryUsage + program.size > stats.memory_slots) {
            return { success: false, message: "Insufficient memory slots" };
        }
        
        // Check processing power requirements
        if (program.requirements.processing_power > stats.processing_power) {
            return { success: false, message: "Insufficient processing power" };
        }
        
        // Check program limit
        if (this.playerDeck.installed_programs.length >= stats.max_programs) {
            return { success: false, message: "Maximum programs installed" };
        }
        
        // Check if already installed
        if (this.playerDeck.installed_programs.includes(programKey)) {
            return { success: false, message: "Program already installed" };
        }
        
        this.playerDeck.installed_programs.push(programKey);
        return { 
            success: true, 
            message: `${program.name} successfully installed`,
            memoryUsed: currentMemoryUsage + program.size,
            memoryTotal: stats.memory_slots
        };
    }
    
    // Uninstall a program  
    uninstallProgram(programKey) {
        const index = this.playerDeck.installed_programs.indexOf(programKey);
        if (index === -1) {
            return { success: false, message: "Program not installed" };
        }
        
        this.playerDeck.installed_programs.splice(index, 1);
        const program = this.programs[programKey];
        return { 
            success: true, 
            message: `${program.name} uninstalled`,
            memoryFreed: program.size
        };
    }
    
    // Install hardware upgrade
    installHardware(hardwareKey) {
        const hardware = this.hardware[hardwareKey];
        if (!hardware) return { success: false, message: "Hardware not found" };
        
        const baseDeck = this.deckTypes[this.playerDeck.base_deck];
        const availableSlots = baseDeck.upgradeSlots[hardware.type] - 
                              this.playerDeck.used_upgrade_slots[hardware.type];
        
        if (hardware.requirements.upgrade_slots > availableSlots) {
            return { 
                success: false, 
                message: `Insufficient ${hardware.type} upgrade slots` 
            };
        }
        
        if (this.playerDeck.installed_hardware.includes(hardwareKey)) {
            return { success: false, message: "Hardware already installed" };
        }
        
        this.playerDeck.installed_hardware.push(hardwareKey);
        this.playerDeck.used_upgrade_slots[hardware.type] += hardware.requirements.upgrade_slots;
        
        return { 
            success: true, 
            message: `${hardware.name} successfully installed`,
            statsChanged: this.getStatChanges(hardware.effect)
        };
    }
    
    // Calculate current memory usage
    calculateMemoryUsage() {
        return this.playerDeck.installed_programs.reduce((total, programKey) => {
            const program = this.programs[programKey];
            return total + (program ? program.size : 0);
        }, 0);
    }
    
    // Get program effectiveness against specific ICE type
    getProgramEffectiveness(programKey, iceType) {
        const program = this.programs[programKey];
        if (!program || !program.effectiveness) return 1.0;
        
        return program.effectiveness[iceType] || 1.0;
    }
    
    // Simulate program execution
    executeProgram(programKey, target = null) {
        const program = this.programs[programKey];
        if (!program) return { success: false, message: "Program not found" };
        
        if (!this.playerDeck.installed_programs.includes(programKey)) {
            return { success: false, message: "Program not installed" };
        }
        
        // Increase heat
        this.playerDeck.heat_level = Math.min(100, this.playerDeck.heat_level + 5);
        
        // Decrease condition slightly
        this.playerDeck.condition = Math.max(0, this.playerDeck.condition - 0.1);
        
        const result = {
            success: true,
            program: program.name,
            execution_time: program.stats.execution_time || 1,
            heat_generated: 5,
            effects: []
        };
        
        // Apply program-specific effects
        switch (program.type) {
            case "attack":
                if (target && target.iceType) {
                    const effectiveness = this.getProgramEffectiveness(programKey, target.iceType);
                    const finalDamage = program.stats.attack_power * effectiveness;
                    result.damage = finalDamage;
                    result.accuracy = program.stats.accuracy;
                    result.stealth_impact = program.stats.stealth;
                }
                break;
                
            case "defense":
                result.defense_bonus = program.stats.defense_bonus;
                result.duration = program.stats.duration;
                break;
                
            case "stealth":
                result.stealth_bonus = program.stats.stealth_bonus;
                result.duration = program.stats.duration;
                break;
                
            case "utility":
                result.utility_effect = program.category;
                break;
        }
        
        return result;
    }
    
    // Deck maintenance and repair
    performMaintenance() {
        const maintenanceCost = Math.floor((100 - this.playerDeck.condition) * 50);
        
        this.playerDeck.condition = Math.min(100, this.playerDeck.condition + 20);
        this.playerDeck.heat_level = Math.max(0, this.playerDeck.heat_level - 30);
        
        return {
            cost: maintenanceCost,
            condition_restored: 20,
            heat_reduced: 30,
            message: "Deck maintenance completed"
        };
    }
    
    // Cool down deck
    coolDown(time_minutes = 10) {
        const heatReduction = Math.min(this.playerDeck.heat_level, time_minutes * 2);
        this.playerDeck.heat_level -= heatReduction;
        
        return {
            heat_reduced: heatReduction,
            current_heat: this.playerDeck.heat_level,
            message: `Deck cooled for ${time_minutes} minutes`
        };
    }
    
    // Get available upgrades
    getAvailableUpgrades() {
        const baseDeck = this.deckTypes[this.playerDeck.base_deck];
        const available = {
            programs: [],
            hardware: []
        };
        
        // Available programs (not installed)
        Object.keys(this.programs).forEach(programKey => {
            if (!this.playerDeck.installed_programs.includes(programKey)) {
                const program = this.programs[programKey];
                const stats = this.getEffectiveDeckStats();
                const canInstall = (
                    program.requirements.processing_power <= stats.processing_power &&
                    this.calculateMemoryUsage() + program.size <= stats.memory_slots &&
                    this.playerDeck.installed_programs.length < stats.max_programs
                );
                
                available.programs.push({
                    key: programKey,
                    ...program,
                    can_install: canInstall
                });
            }
        });
        
        // Available hardware (not installed)
        Object.keys(this.hardware).forEach(hardwareKey => {
            if (!this.playerDeck.installed_hardware.includes(hardwareKey)) {
                const hardware = this.hardware[hardwareKey];
                const availableSlots = baseDeck.upgradeSlots[hardware.type] - 
                                      this.playerDeck.used_upgrade_slots[hardware.type];
                const canInstall = hardware.requirements.upgrade_slots <= availableSlots;
                
                available.hardware.push({
                    key: hardwareKey,
                    ...hardware,
                    can_install: canInstall,
                    slots_required: hardware.requirements.upgrade_slots,
                    slots_available: availableSlots
                });
            }
        });
        
        return available;
    }
    
    // Helper methods
    getStatChanges(effect) {
        return Object.keys(effect).map(stat => `${stat}: ${effect[stat] > 0 ? '+' : ''}${effect[stat]}`);
    }
    
    getDeckSummary() {
        const baseDeck = this.deckTypes[this.playerDeck.base_deck];
        const stats = this.getEffectiveDeckStats();
        const memoryUsed = this.calculateMemoryUsage();
        
        return {
            deck_name: baseDeck.name,
            manufacturer: baseDeck.manufacturer,
            condition: this.playerDeck.condition,
            heat_level: this.playerDeck.heat_level,
            stats: stats,
            memory_usage: `${memoryUsed}/${stats.memory_slots}`,
            programs_installed: this.playerDeck.installed_programs.length,
            max_programs: stats.max_programs,
            installed_programs: this.playerDeck.installed_programs.map(key => this.programs[key]?.name || key),
            installed_hardware: this.playerDeck.installed_hardware.map(key => this.hardware[key]?.name || key)
        };
    }
    
    // Export/import for save games
    exportDeck() {
        return JSON.parse(JSON.stringify(this.playerDeck));
    }
    
    importDeck(deckData) {
        this.playerDeck = { ...deckData };
    }
}