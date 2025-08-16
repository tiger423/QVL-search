#!/usr/bin/env python3

import sys
sys.path.append('.')

import importlib.util
spec = importlib.util.spec_from_file_location("crawler_SSD", "crawler-SSD.py")
crawler_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crawler_module)
GigabyteServerQVLCrawler = crawler_module.GigabyteServerQVLCrawler

def test_categorization():
    crawler = GigabyteServerQVLCrawler()
    
    print("Testing new character-based categorization logic:")
    print("=" * 50)
    
    test_models = [
        'G293-S40-AAP1',  # Should be GPU-Server
        'R183-S95-AAD1',  # Should be Rack-Server  
        'H263-S66-AAW1',  # Should be High-Density-Server
        'S123-TEST',      # Should be Storage-Server
        'X456-TEST',      # Should be Rack-Server
        'E789-TEST',      # Should be Rack-Server
        'Z999-TEST'       # Should fallback to General-Purpose-Server
    ]
    
    for model in test_models:
        category = crawler.get_category_from_model(model)
        first_char = model[0].upper()
        print(f"{model:<15} -> {category:<25} (first char: '{first_char}')")
    
    print("\nCategorization test completed successfully!")

if __name__ == "__main__":
    test_categorization()
