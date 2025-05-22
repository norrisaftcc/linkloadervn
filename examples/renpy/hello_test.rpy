# Simple Ren'Py test
define s = Character("Slim")

label start:
    s "Hello world! I'm Slim."
    s "This is a test of the conversion pipeline."
    
    menu:
        "What should I do?"
        
        "Say goodbye":
            s "Goodbye!"
            return
            
        "Ask a question":
            s "What would you like to know?"
            s "Actually, that's all for now."
            return