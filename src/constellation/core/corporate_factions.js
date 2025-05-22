/**
 * Corporate Faction System
 * Defines the major megacorps and their characteristics in the cyberpunk world
 */

export class CorporateFactions {
    constructor() {
        this.factions = this.initializeFactions();
        this.playerRelations = new Map(); // Track player standing with each corp
        this.corporateEvents = [];
        this.initializeRelations();
    }
    
    initializeFactions() {
        return {
            ARASAKA: {
                name: "Arasaka Corporation",
                founded: 2020,
                headquarters: "Night City, NUSA",
                ceo: "Saburo Arasaka",
                logo: "corporate_red_mountain.svg",
                colors: {
                    primary: "#FF0000",
                    secondary: "#8B0000", 
                    accent: "#FFD700"
                },
                specialties: [
                    "Corporate Security",
                    "Neural Interface Technology", 
                    "Banking & Finance",
                    "Mercenary Services"
                ],
                preferredICE: ["SENTRY_ICE", "BLACK_ICE"],
                securityLevel: "MAXIMUM",
                corporateCulture: "authoritarian_traditional",
                resources: {
                    military: 10,
                    technology: 9,
                    finance: 10,
                    influence: 9
                },
                enemyFactions: ["MILITECH", "BIOTECHNICA"],
                alliedFactions: ["KANG_TAO"],
                reputation: {
                    public: "powerful_but_feared",
                    underground: "primary_target",
                    description: "The most powerful and feared megacorp in the world. Known for ruthless efficiency and traditional Japanese corporate values."
                },
                secretProjects: [
                    "Soul Killer Technology",
                    "Digital Immortality Research", 
                    "Neural Network Control Systems"
                ],
                networkSecurity: {
                    layers: 7,
                    responseTime: "immediate",
                    traceCapability: "world_class",
                    countermeasures: "lethal_authorized"
                }
            },
            
            MILITECH: {
                name: "Militech International",
                founded: 1996,
                headquarters: "Washington DC, NUSA", 
                ceo: "General Donald Lundee",
                logo: "militech_eagle.svg",
                colors: {
                    primary: "#008000",
                    secondary: "#556B2F",
                    accent: "#FFD700"
                },
                specialties: [
                    "Military Hardware",
                    "Weapons Manufacturing",
                    "Defense Contracts", 
                    "Tactical Software"
                ],
                preferredICE: ["BLOODHOUND_ICE", "WALL_ICE"],
                securityLevel: "EXTREME",
                corporateCulture: "military_industrial",
                resources: {
                    military: 10,
                    technology: 8,
                    finance: 8,
                    influence: 7
                },
                enemyFactions: ["ARASAKA", "ZETATECH"],
                alliedFactions: ["PETROCHEM"],
                reputation: {
                    public: "patriotic_defender",
                    underground: "war_profiteer",
                    description: "The NUSA's premier military contractor. Combines cutting-edge weapons tech with old-school military discipline."
                },
                secretProjects: [
                    "Autonomous Weapon Systems",
                    "Soldier Enhancement Programs",
                    "Urban Warfare AI"
                ],
                networkSecurity: {
                    layers: 6,
                    responseTime: "rapid",
                    traceCapability: "military_grade",
                    countermeasures: "kinetic_response_authorized"
                }
            },
            
            BIOTECHNICA: {
                name: "Biotechnica",
                founded: 2003,
                headquarters: "Rome, Italy",
                ceo: "Dr. Alessandro Fortuna",
                logo: "biotech_dna_helix.svg",
                colors: {
                    primary: "#9980FA",
                    secondary: "#663399",
                    accent: "#00FFFF"
                },
                specialties: [
                    "Biotechnology Research",
                    "Pharmaceutical Development",
                    "Genetic Engineering",
                    "Agricultural Innovation"
                ],
                preferredICE: ["SPHINX_ICE", "PHANTOM_ICE"],
                securityLevel: "HIGH",
                corporateCulture: "scientific_progressive",
                resources: {
                    military: 4,
                    technology: 10,
                    finance: 7,
                    influence: 6
                },
                enemyFactions: ["ARASAKA", "PETROCHEM"],
                alliedFactions: ["ZETATECH"],
                reputation: {
                    public: "life_saving_innovator",
                    underground: "genetic_manipulator",
                    description: "Leading biotech corp focused on extending and enhancing human life through genetic and pharmaceutical breakthroughs."
                },
                secretProjects: [
                    "Human Genetic Optimization",
                    "Artificial Organism Creation",
                    "Neural Enhancement Drugs"
                ],
                networkSecurity: {
                    layers: 5,
                    responseTime: "delayed",
                    traceCapability: "sophisticated",
                    countermeasures: "biological_hazard_protocols"
                }
            },
            
            ZETATECH: {
                name: "ZetaTech",
                founded: 2025,
                headquarters: "Los Angeles, Free State",
                ceo: "Marcus Webb",
                logo: "zetatech_circuit.svg",
                colors: {
                    primary: "#00FFFF",
                    secondary: "#008B8B",
                    accent: "#FFE4B5"
                },
                specialties: [
                    "Cybernetic Implants",
                    "Neural Interfaces",
                    "Brain-Computer Interfaces",
                    "Consciousness Research"
                ],
                preferredICE: ["PHANTOM_ICE", "SENTRY_ICE"],
                securityLevel: "HIGH",
                corporateCulture: "tech_libertarian",
                resources: {
                    military: 5,
                    technology: 9,
                    finance: 6,
                    influence: 5
                },
                enemyFactions: ["MILITECH", "KANG_TAO"],
                alliedFactions: ["BIOTECHNICA"],
                reputation: {
                    public: "human_augmentation_pioneer",
                    underground: "body_modification_extremist",
                    description: "Cutting-edge cybernetics corp pushing the boundaries of human-machine integration."
                },
                secretProjects: [
                    "Full Body Conversion Technology",
                    "Consciousness Transfer Protocols",
                    "Artificial Soul Development"
                ],
                networkSecurity: {
                    layers: 5,
                    responseTime: "moderate",
                    traceCapability: "advanced",
                    countermeasures: "neural_feedback_loops"
                }
            },
            
            KANG_TAO: {
                name: "Kang Tao Corporation",
                founded: 2042,
                headquarters: "Heywood, Night City",
                ceo: "Arthur Jenkins",
                logo: "kangtao_shield.svg",
                colors: {
                    primary: "#FFD700",
                    secondary: "#B8860B",
                    accent: "#FF0000"
                },
                specialties: [
                    "Smart Weapons",
                    "Drone Technology", 
                    "AI Development",
                    "Automated Defense Systems"
                ],
                preferredICE: ["WALL_ICE", "BLACK_ICE"],
                securityLevel: "EXTREME",
                corporateCulture: "authoritarian_efficiency",
                resources: {
                    military: 8,
                    technology: 8,
                    finance: 7,
                    influence: 6
                },
                enemyFactions: ["ZETATECH", "BIOTECHNICA"],
                alliedFactions: ["ARASAKA"],
                reputation: {
                    public: "smart_weapon_innovator",
                    underground: "surveillance_state_enabler",
                    description: "Specialist in AI-driven weapons and surveillance technology. Known for their 'smart' weapon systems."
                },
                secretProjects: [
                    "Autonomous Hunter-Killer Drones",
                    "Predictive Crime AI",
                    "Mass Surveillance Networks"
                ],
                networkSecurity: {
                    layers: 6,
                    responseTime: "immediate",
                    traceCapability: "predictive",
                    countermeasures: "automated_response_grid"
                }
            },
            
            PETROCHEM: {
                name: "Petrochem",
                founded: 1998,
                headquarters: "Texas, NUSA",
                ceo: "Buck Morrison",
                logo: "petrochem_flame.svg", 
                colors: {
                    primary: "#FF8C00",
                    secondary: "#FF4500",
                    accent: "#000000"
                },
                specialties: [
                    "Energy Production",
                    "Chemical Processing",
                    "Fuel Technology",
                    "Environmental Engineering"
                ],
                preferredICE: ["WALL_ICE", "SENTRY_ICE"],
                securityLevel: "MEDIUM",
                corporateCulture: "old_energy_conservative",
                resources: {
                    military: 6,
                    technology: 6,
                    finance: 9,
                    influence: 8
                },
                enemyFactions: ["BIOTECHNICA"],
                alliedFactions: ["MILITECH"],
                reputation: {
                    public: "energy_provider",
                    underground: "environmental_destroyer",
                    description: "Traditional energy giant adapting to the new world. Massive resources but older technology."
                },
                secretProjects: [
                    "Fusion Reactor Miniaturization",
                    "Climate Control Technology",
                    "Synthetic Fuel Development"
                ],
                networkSecurity: {
                    layers: 4,
                    responseTime: "slow",
                    traceCapability: "basic",
                    countermeasures: "financial_retaliation"
                }
            }
        };
    }
    
    initializeRelations() {
        // Initialize neutral relations with all factions
        Object.keys(this.factions).forEach(factionKey => {
            this.playerRelations.set(factionKey, {
                standing: 0, // -100 to +100
                reputation: "unknown",
                contracts: [],
                hostileActions: 0,
                helpfulActions: 0,
                lastInteraction: null
            });
        });
    }
    
    // Get faction by key
    getFaction(factionKey) {
        return this.factions[factionKey] || null;
    }
    
    // Get all factions
    getAllFactions() {
        return this.factions;
    }
    
    // Get player's relationship with a faction
    getPlayerRelation(factionKey) {
        return this.playerRelations.get(factionKey);
    }
    
    // Modify player's standing with a faction
    modifyStanding(factionKey, change, reason = "") {
        const relation = this.playerRelations.get(factionKey);
        if (!relation) return false;
        
        const oldStanding = relation.standing;
        relation.standing = Math.max(-100, Math.min(100, relation.standing + change));
        relation.lastInteraction = {
            change: change,
            reason: reason,
            timestamp: Date.now()
        };
        
        // Update reputation tier
        if (relation.standing >= 75) relation.reputation = "allied";
        else if (relation.standing >= 25) relation.reputation = "friendly";
        else if (relation.standing >= -25) relation.reputation = "neutral";
        else if (relation.standing >= -75) relation.reputation = "hostile";
        else relation.reputation = "enemy";
        
        // Track action types
        if (change > 0) relation.helpfulActions++;
        else if (change < 0) relation.hostileActions++;
        
        // Handle faction relationships (enemy/ally effects)
        this.propagateFactionalEffects(factionKey, change, reason);
        
        return {
            faction: factionKey,
            oldStanding: oldStanding,
            newStanding: relation.standing,
            reputationChange: this.getReputationDescription(oldStanding, relation.standing),
            secondaryEffects: this.getSecondaryEffects(factionKey, change)
        };
    }
    
    propagateFactionalEffects(primaryFaction, change, reason) {
        const faction = this.factions[primaryFaction];
        if (!faction) return;
        
        // Affect allied factions (smaller positive effect)
        faction.alliedFactions.forEach(allyKey => {
            if (change > 0) {
                this.modifyStanding(allyKey, Math.ceil(change * 0.3), `Allied with ${faction.name}: ${reason}`);
            }
        });
        
        // Affect enemy factions (smaller negative effect)
        faction.enemyFactions.forEach(enemyKey => {
            if (change > 0) {
                this.modifyStanding(enemyKey, Math.floor(change * -0.2), `Enemy of ${faction.name}: ${reason}`);
            } else if (change < 0) {
                this.modifyStanding(enemyKey, Math.ceil(change * -0.1), `Enemy of ${faction.name}: ${reason}`);
            }
        });
    }
    
    getReputationDescription(oldStanding, newStanding) {
        const getRepTier = (standing) => {
            if (standing >= 75) return "Allied";
            if (standing >= 25) return "Friendly"; 
            if (standing >= -25) return "Neutral";
            if (standing >= -75) return "Hostile";
            return "Enemy";
        };
        
        const oldTier = getRepTier(oldStanding);
        const newTier = getRepTier(newStanding);
        
        if (oldTier !== newTier) {
            return `Reputation changed from ${oldTier} to ${newTier}`;
        }
        return null;
    }
    
    getSecondaryEffects(factionKey, change) {
        const effects = [];
        const faction = this.factions[factionKey];
        
        // Check for unlocked opportunities
        const standing = this.playerRelations.get(factionKey).standing;
        
        if (standing >= 25 && change > 0) {
            effects.push("New corporate contracts may be available");
        }
        
        if (standing >= 50 && change > 0) {
            effects.push("Access to faction-specific equipment");
        }
        
        if (standing >= 75 && change > 0) {
            effects.push("Invitation to corporate inner circle");
        }
        
        if (standing <= -25 && change < 0) {
            effects.push("Corporate security may be heightened");
        }
        
        if (standing <= -50 && change < 0) {
            effects.push("Active corporate interference expected");
        }
        
        if (standing <= -75 && change < 0) {
            effects.push("Corporate assassination teams may be deployed");
        }
        
        return effects;
    }
    
    // Generate contextual corporate encounters based on faction standings
    generateCorporateEncounter(scenario = "random") {
        const encounters = [];
        
        // Check each faction for potential encounters
        Object.keys(this.factions).forEach(factionKey => {
            const relation = this.playerRelations.get(factionKey);
            const faction = this.factions[factionKey];
            
            if (relation.reputation === "allied" && Math.random() < 0.3) {
                encounters.push({
                    type: "corporate_offer",
                    faction: factionKey,
                    title: `${faction.name} Corporate Contract`,
                    description: `${faction.name} offers you a high-paying contract leveraging your proven loyalty.`,
                    reward: "substantial_payment_and_standing",
                    risk: "moderate"
                });
            }
            
            if (relation.reputation === "enemy" && Math.random() < 0.4) {
                encounters.push({
                    type: "corporate_retaliation", 
                    faction: factionKey,
                    title: `${faction.name} Security Response`,
                    description: `${faction.name} has had enough of your interference. Expect corporate countermeasures.`,
                    threat: "active_opposition",
                    risk: "high"
                });
            }
            
            if (relation.reputation === "neutral" && Math.random() < 0.2) {
                encounters.push({
                    type: "corporate_recruitment",
                    faction: factionKey, 
                    title: `${faction.name} Talent Scout`,
                    description: `A ${faction.name} recruiter has noticed your skills and wants to discuss opportunities.`,
                    opportunity: "faction_alignment_choice",
                    risk: "low"
                });
            }
        });
        
        return encounters;
    }
    
    // Get corporate context for story scenes
    getCorporateContext(location = "generic") {
        const context = {
            dominantFaction: null,
            securityLevel: "medium",
            corporatePresence: [],
            availableResources: [],
            restrictions: [],
            opportunities: []
        };
        
        // Determine dominant faction based on location
        const locationFactionsMap = {
            "night_city": ["ARASAKA", "KANG_TAO"],
            "corporate_plaza": ["ARASAKA", "MILITECH", "BIOTECHNICA"],
            "tech_district": ["ZETATECH", "BIOTECHNICA"],
            "industrial_zone": ["PETROCHEM", "MILITECH"],
            "financial_center": ["ARASAKA", "PETROCHEM"]
        };
        
        const potentialFactions = locationFactionsMap[location] || Object.keys(this.factions);
        
        // Add corporate presence based on player relations
        potentialFactions.forEach(factionKey => {
            const relation = this.playerRelations.get(factionKey);
            const faction = this.factions[factionKey];
            
            if (relation.reputation === "allied") {
                context.opportunities.push(`${faction.name} resources available`);
                context.availableResources.push(faction.specialties[0]);
            } else if (relation.reputation === "enemy") {
                context.restrictions.push(`${faction.name} security actively hunting you`);
                context.securityLevel = "maximum";
            }
            
            context.corporatePresence.push({
                faction: factionKey,
                name: faction.name,
                influence: relation.reputation,
                securityResponse: faction.networkSecurity.responseTime
            });
        });
        
        return context;
    }
    
    // Corporate war/alliance system
    getCurrentCorporateConflicts() {
        const conflicts = [];
        
        // Check for active conflicts based on faction relations
        Object.keys(this.factions).forEach(factionKey => {
            const faction = this.factions[factionKey];
            faction.enemyFactions.forEach(enemyKey => {
                const playerWithFaction = this.playerRelations.get(factionKey).standing;
                const playerWithEnemy = this.playerRelations.get(enemyKey).standing;
                
                // If player is allied with both enemies, create tension
                if (playerWithFaction > 25 && playerWithEnemy > 25) {
                    conflicts.push({
                        type: "loyalty_conflict",
                        factions: [factionKey, enemyKey],
                        description: `Your loyalty to both ${faction.name} and ${this.factions[enemyKey].name} creates internal corporate tensions.`,
                        consequence: "forced_choice_coming"
                    });
                }
                
                // If player is heavily aligned with one side
                if (playerWithFaction > 50 && playerWithEnemy < -25) {
                    conflicts.push({
                        type: "corporate_war_involvement",
                        ally: factionKey,
                        enemy: enemyKey,
                        description: `Your alliance with ${faction.name} makes you a target for ${this.factions[enemyKey].name} operations.`,
                        consequence: "increased_enemy_activity"
                    });
                }
            });
        });
        
        return conflicts;
    }
    
    // Export/import for save game functionality
    exportRelations() {
        const exportData = {};
        this.playerRelations.forEach((value, key) => {
            exportData[key] = value;
        });
        return exportData;
    }
    
    importRelations(relationData) {
        this.playerRelations.clear();
        Object.keys(relationData).forEach(key => {
            this.playerRelations.set(key, relationData[key]);
        });
    }
}