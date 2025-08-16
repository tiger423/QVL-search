# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import csv
import random
from datetime import datetime

class GigabyteServerQVLCrawler:
    def __init__(self):
        self.base_urls = [
            "https://www.gigabyte.com/tw/Enterprise",
            "https://www.gigabyte.com/Enterprise"
        ]
        self.categories = [
            "Rack-Server",
            "General-Purpose-Server", 
            "GPU-Server",
            "AI-Server",
            "High-Density-Server"
        ]
        self.driver = None
        self.request_count = 0
        
    def get_converted_server_list(self):
        """Get the full converted server list"""
        server_models = [
            "G293-S40-AAP1", "G293-S41-AAP1", "G293-S42-AAP1", "G293-S43-AAP1", "G293-S45-AAP1",
            "G293-S46-AAM1", "G293-S47-AAP1", "H263-S66-AAW1", "H263-S67-AAW1", "G363-SR0-AAX1",
            "G363-SR0-AAX4", "G363-SR0-LAX1", "G363-SR0-LAX4", "R183-S95-AAD1", "R183-S95-AAV1",
            "R183-S96-AAD1", "R183-S96-AAV1", "R183-S97-AAD1", "R183-S97-AAV1", "R283-S96-AAE1",
            "R283-S96-AAJ1", "R283-S97-AAD1", "R283-S97-AAV1", "R283-S98-AAE1", "R283-S98-AAE2",
            "R283-S98-AAJ1", "R283-S98-AAJ2", "G493-SB0-AAP1", "G493-SB1-AAP1", "G493-SB2-AAP1",
            "G493-SB3-AAP1", "G493-SB4-AAP1", "G593-SD0-AAX1", "G593-SD0-LAX1", "G593-SD2-AAX1",
            "G593-SD2-LAX1", "G593-SD1-AAX1", "G593-SD1-AAX3", "G593-SD1-LAX1", "G593-SD1-LAX3",
            "G593-SX1-AAX1", "G4L3-SD1-LAX3", "G4L3-SD1-LAX5", "G893-SD1-AAX3", "G893-SD1-AAX5",
            "G893-SG1-AAX1", "R183-SF0-AAJ1", "R183-SF1-AAJ1", "R283-SF0-AAL1", "R283-SF1-AAL1",
            "G383-R80-AAP1", "G293-Z20-AAP1", "G293-Z21-AAP1", "G293-Z22-AAP1", "G293-Z23-AAM1",
            "G293-Z40-AAP1", "G293-Z41-AAP1", "G293-Z42-AAP1", "G293-Z43-AAP1", "H273-Z84-AAW1",
            "H273-Z85-AAW1", "H273-Z85-LAZ1", "G363-ZR0-AAX1", "G363-ZR0-ACX4", "G363-ZR0-LAX1",
            "G363-ZR0-LCX4", "R183-Z93-AAD1", "R183-Z93-AAV1", "R183-Z93-LAJ1", "R183-Z94-AAD1",
            "R183-Z94-AAD2", "R183-Z94-AAV1", "R183-Z94-AAV2", "R183-Z95-AAD1", "R183-Z95-AAV1",
            "R183-Z96-AAD1", "R183-Z96-AAV1", "R283-Z94-AAD1", "R283-Z94-AAD2", "R283-Z94-AAV1",
            "R283-Z94-AAV2", "R283-Z95-AAD1", "R283-Z95-AAV1", "R283-Z96-AAE1", "R283-Z96-AAE2",
            "R283-Z96-AAE3", "R283-Z96-AAJ1", "R283-Z96-AAJ2", "R283-Z96-AAJ3", "R283-Z97-AAF1",
            "R283-Z97-AAL1", "G493-ZB1-AAP1", "G493-ZB2-AAP1", "G493-ZB3-AAP1", "G493-ZB4-AAP1",
            "G593-ZD1-AAX1", "G593-ZD1-AAX3", "G593-ZD1-LAX1", "G593-ZD1-LAX3", "G593-ZD2-ABX1",
            "G593-ZD2-ACX1", "G593-ZD2-LBX1", "G593-ZD2-LCX1", "G593-ZX1-AAX1", "R183-ZF0-AAJ1",
            "R183-ZF1-AAJ1", "R283-ZF0-AAL1", "R283-ZF1-AAL1", "G294-Z21-AAP1", "G294-Z21-AAP2",
            "G294-Z22-AAP1", "G294-Z22-AAP2", "G294-Z41-AAP1", "G294-Z41-AAP2", "G294-Z42-AAP1",
            "G294-Z42-AAP2", "G294-Z43-AAP1", "G294-Z43-AAP2", "G494-ZB1-AAP2", "G494-ZB4-AAP2",
            "G4L3-ZD1-LAX3", "G4L3-ZD1-LAX5", "G4L3-ZX1-LAX1", "G4L3-ZX1-LAX2", "G893-ZD1-AAX3",
            "G893-ZD1-AAX5", "G893-ZX1-AAX1", "G893-ZX1-AAX2", "R183-ZK0-AAL1", "R183-ZK0-LAJ1",
            "R283-ZK0-AAL1", "XV23-ZX0-AAJ1", "H174-A80-LAS1", "H274-A81-LAZ1", "H374-A80-AAW1",
            "H374-A80-LAW1", "H374-A81-AAW1", "H374-A81-LAW1", "E284-A90-AAJ1", "R184-A90-AAJ1",
            "R184-A92-AAJ1", "R184-A92-LAJ1", "R284-A90-AAL1", "R284-A90-AAL2", "R284-A92-AAL1",
            "R284-A93-AAS1", "R284-A94-AAL1", "G894-AD1-AAX5", "XV24-AX0-AAJ1", "G294-S41-AAP1",
            "G294-S41-AAP2", "G294-S42-AAP1", "G294-S42-AAP2", "G294-S43-AAP1", "G294-S43-AAP2",
            "H274-S60-AAW1", "H274-S60-LAW1", "H274-S61-AAW1", "H274-S61-LAW1", "E284-S90-AAJ1",
            "R184-S90-AAV1", "R184-S91-AAV1", "R184-S92-AAV1", "R184-S92-LAV1", "R284-S90-AAJ1",
            "R284-S92-AAJ1", "R284-S93-AAL1", "G494-SB0-AAP1", "G494-SB0-AAP2", "G494-SB1-AAP2",
            "G494-SB3-AAP1", "G494-SB4-AAP2", "G4L4-SD1-LAX5", "G894-SD1-AAX5", "R184-SF1-AAJ1",
            "R284-SF0-AAL1", "XV24-SX0-AAJ1"
        ]
        return server_models
    
    def setup_selenium_driver(self):
        """Setup Selenium WebDriver with headless configuration"""
        if self.driver is None:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--window-size=1920,1080")
            options.add_argument(f"--user-data-dir=/tmp/chrome_user_data_{random.randint(1000, 9999)}")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.set_page_load_timeout(30)
    
    def has_qvl(self, page_source):
        """Simple check: does the page contain the word 'QVL'? - SAME AS test_qvl_detection()"""
        return 'QVL' in page_source
    
    def clean_data_for_csv(self, data):
        """Clean data to ensure it can be saved to CSV without numpy errors"""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                cleaned[key] = self.clean_value_for_csv(value)
            return cleaned
        elif isinstance(data, list):
            return [self.clean_data_for_csv(item) for item in data]
        else:
            return self.clean_value_for_csv(data)
    
    def clean_value_for_csv(self, value):
        """Clean individual values for CSV compatibility"""
        if value is None:
            return ''
        elif hasattr(value, 'tolist'):  # numpy array
            return str(value.tolist())
        elif hasattr(value, '__iter__') and not isinstance(value, str):  # other iterables
            return str(list(value))
        else:
            return str(value)
    
    def check_server_exists(self, server_model):
        """FIXED: Use EXACT SAME algorithm as test_qvl_detection() with delays"""
        print(f"Checking server: {server_model}")
        
        if self.driver is None:
            self.setup_selenium_driver()
        
        # Try all combinations of base_url and category - SAME AS test_qvl_detection()
        for base_url in self.base_urls:
            for category in self.categories:
                test_url = f"{base_url}/{category}/{server_model}"
                print(f"  Testing: {test_url}")
                
                try:
                    # SAME AS test_qvl_detection() - simple approach
                    self.driver.get(test_url)
                    
                    # Add delay between requests - this was missing in test_qvl_detection()
                    delay = random.uniform(2, 4)
                    print(f"    Waiting {delay:.1f} seconds...")
                    time.sleep(delay)
                    
                    # EXACT SAME logic as test_qvl_detection()
                    page_source = self.driver.page_source
                    has_qvl = self.has_qvl(page_source)
                    
                    print(f"    Page loaded: YES")
                    print(f"    Has 'QVL' in content: {'YES' if has_qvl else 'NO'}")
                    
                    # Show some context around QVL if found - SAME AS test_qvl_detection()
                    if has_qvl:
                        lines = page_source.split('\n')
                        qvl_lines = [line.strip() for line in lines if 'QVL' in line]
                        print(f"    QVL references found: {len(qvl_lines)}")
                        
                        print(f"  ? FOUND (has QVL): {test_url}")
                        return test_url, category
                    else:
                        print(f"    No QVL found in page content")
                        
                except Exception as e:
                    print(f"    Error: {e}")
                    continue
                
                # Small delay between different URL attempts
                time.sleep(1)
        
        print(f"  ? NOT FOUND: {server_model}")
        return None, None
    
    def save_valid_servers_csv(self, found_servers):
        """Save the list of valid servers after Phase 1 as CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"valid_servers_list_{timestamp}.csv"
        
        try:
            print(f"Saving {len(found_servers)} servers to CSV...")
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if not found_servers:
                    print("?? No servers to save")
                    return None
                
                fieldnames = ['Server_Model', 'Server_URL', 'Category', 'Status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for server in found_servers:
                    clean_row = {}
                    for field in fieldnames:
                        value = server.get(field, '')
                        clean_row[field] = self.clean_value_for_csv(value)
                    writer.writerow(clean_row)
            
            found_count = len([server for server in found_servers if server.get('Status') == 'Found'])
            not_found_count = len(found_servers) - found_count
            
            print(f"? Valid servers list saved to CSV: {filename}")
            print(f"   Total servers: {len(found_servers)}")
            print(f"   Found: {found_count}")
            print(f"   Not found: {not_found_count}")
            
            return filename
            
        except Exception as e:
            print(f"? Error saving valid servers CSV: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_qvl_data_batch_csv(self, all_qvl_data, batch_number, total_batches):
        """Save QVL data every 10 servers as CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qvl_data_batch_{batch_number}_of_{total_batches}_{timestamp}.csv"
        
        try:
            if not all_qvl_data:
                print(f"?? No QVL data to save for batch {batch_number}")
                return None, []
            
            print(f"Saving batch {batch_number} with {len(all_qvl_data)} entries to CSV...")
            
            trusta_matches = self.search_trusta_in_data(all_qvl_data)
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                all_fields = set()
                for item in all_qvl_data:
                    all_fields.update(item.keys())
                
                all_fields.update(['Batch_Number', 'Total_Batches', 'Save_Timestamp', 'Has_TRUSTA_Match', 'Has_T7P5_Match'])
                
                fieldnames = sorted(list(all_fields))
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for item in all_qvl_data:
                    clean_row = {}
                    
                    for field in fieldnames:
                        value = item.get(field, '')
                        clean_row[field] = self.clean_value_for_csv(value)
                    
                    clean_row['Batch_Number'] = str(batch_number)
                    clean_row['Total_Batches'] = str(total_batches)
                    clean_row['Save_Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    has_trusta = False
                    has_t7p5 = False
                    for match in trusta_matches:
                        if (match.get('Server_Model') == item.get('Server_Model') and
                            match.get('Table_Number') == item.get('Table_Number') and
                            match.get('Row_Number') == item.get('Row_Number')):
                            has_trusta = match.get('Has_TRUSTA', False)
                            has_t7p5 = match.get('Has_T7P5', False)
                            break
                    
                    clean_row['Has_TRUSTA_Match'] = str(has_trusta)
                    clean_row['Has_T7P5_Match'] = str(has_t7p5)
                    
                    writer.writerow(clean_row)
            
            print(f"? Batch {batch_number} QVL data saved to CSV: {filename}")
            print(f"   QVL entries: {len(all_qvl_data)}")
            print(f"   TRUSTA/T7P5 matches: {len(trusta_matches)}")
            print(f"   Servers in batch: {len(set([item.get('Server_Model', '') for item in all_qvl_data]))}")
            
            return filename, trusta_matches
            
        except Exception as e:
            print(f"? Error saving batch {batch_number} QVL CSV: {e}")
            import traceback
            traceback.print_exc()
            return None, []
    
    def crawl_server_qvl(self, server_url, server_model):
        """Crawl QVL data for a specific server - SAME AS test_qvl_detection()"""
        qvl_url = f"{server_url}/Support-QVL?CAT=Storage-NVMeSSD"
        
        print(f"  Testing QVL crawling for: {server_model}")
        print(f"  QVL URL: {qvl_url}")
        
        try:
            if self.driver is None:
                self.setup_selenium_driver()
            
            # SAME AS test_qvl_detection()
            self.driver.get(qvl_url)
            time.sleep(5)
            
            # Parse page content
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract table data
            tables = soup.find_all('table')
            print(f"    Found {len(tables)} tables")
            
            all_data = []
            
            for table_idx, table in enumerate(tables):
                rows = table.find_all('tr')
                if len(rows) < 2:
                    continue
                
                # Get headers
                headers = []
                for th in rows[0].find_all(['th', 'td']):
                    header_text = th.get_text(strip=True)
                    headers.append(header_text if header_text else f"Col_{len(headers)+1}")
                
                # Get data rows
                for row_idx, row in enumerate(rows[1:], 1):
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_dict = {
                            'Server_Model': server_model,
                            'Server_URL': server_url,
                            'QVL_URL': qvl_url,
                            'Table_Number': table_idx + 1,
                            'Row_Number': row_idx
                        }
                        
                        for i, cell in enumerate(cells):
                            header = headers[i] if i < len(headers) else f'Column_{i+1}'
                            cell_text = cell.get_text(strip=True)
                            row_dict[header] = cell_text
                        
                        all_data.append(row_dict)
            
            print(f"    QVL entries found: {len(all_data)}")
            
            if all_data:
                # Search for TRUSTA/T7P5 - SAME AS test_qvl_detection()
                matches = self.search_trusta_in_data(all_data)
                print(f"    TRUSTA/T7P5 matches: {len(matches)}")
                
                if matches:
                    for match in matches:
                        print(f"      Match found in server: {match.get('Server_Model')}")
            
            return all_data
            
        except Exception as e:
            print(f"    Error crawling {server_model}: {e}")
            return []
    
    def search_trusta_in_data(self, data):
        """Search for TRUSTA/T7P5 in the data"""
        matches = []
        
        for row in data:
            row_text = ""
            for col, value in row.items():
                if value and str(value).strip():
                    row_text += str(value) + " "
            
            row_text = row_text.upper()
            
            if 'TRUSTA' in row_text or 'T7P5' in row_text:
                match_info = row.copy()
                match_info['Has_TRUSTA'] = 'TRUSTA' in row_text
                match_info['Has_T7P5'] = 'T7P5' in row_text
                matches.append(match_info)
        
        return matches
    
    def save_final_results_csv(self, all_data, trusta_matches, found_servers):
        """Save final consolidated results as CSV files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        files_created = []
        
        # 1. All QVL Data CSV
        if all_data:
            all_data_file = f"final_all_qvl_data_{timestamp}.csv"
            try:
                clean_all_data = self.clean_data_for_csv(all_data)
                
                with open(all_data_file, 'w', newline='', encoding='utf-8') as csvfile:
                    if clean_all_data:
                        all_fields = set()
                        for item in clean_all_data:
                            all_fields.update(item.keys())
                        
                        fieldnames = sorted(list(all_fields))
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for item in clean_all_data:
                            clean_row = {}
                            for field in fieldnames:
                                clean_row[field] = self.clean_value_for_csv(item.get(field, ''))
                            writer.writerow(clean_row)
                
                files_created.append(('All QVL Data', all_data_file))
                print(f"? All QVL data saved to CSV: {all_data_file}")
                
            except Exception as e:
                print(f"? Error saving all QVL data CSV: {e}")
        
        # 2. TRUSTA/T7P5 Matches CSV
        if trusta_matches:
            matches_file = f"final_trusta_t7p5_matches_{timestamp}.csv"
            try:
                clean_matches = self.clean_data_for_csv(trusta_matches)
                
                with open(matches_file, 'w', newline='', encoding='utf-8') as csvfile:
                    if clean_matches:
                        all_fields = set()
                        for item in clean_matches:
                            all_fields.update(item.keys())
                        
                        fieldnames = sorted(list(all_fields))
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for item in clean_matches:
                            clean_row = {}
                            for field in fieldnames:
                                clean_row[field] = self.clean_value_for_csv(item.get(field, ''))
                            writer.writerow(clean_row)
                
                files_created.append(('TRUSTA/T7P5 Matches', matches_file))
                print(f"? TRUSTA/T7P5 matches saved to CSV: {matches_file}")
                
            except Exception as e:
                print(f"? Error saving matches CSV: {e}")
        
        # 3. Server Discovery Results CSV
        if found_servers:
            servers_file = f"final_server_discovery_{timestamp}.csv"
            try:
                clean_servers = self.clean_data_for_csv(found_servers)
                
                with open(servers_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Server_Model', 'Server_URL', 'Category', 'Status']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for server in clean_servers:
                        clean_row = {}
                        for field in fieldnames:
                            clean_row[field] = self.clean_value_for_csv(server.get(field, ''))
                        writer.writerow(clean_row)
                
                files_created.append(('Server Discovery', servers_file))
                print(f"? Server discovery results saved to CSV: {servers_file}")
                
            except Exception as e:
                print(f"? Error saving server discovery CSV: {e}")
        
        # 4. Summary Statistics CSV
        summary_file = f"final_summary_statistics_{timestamp}.csv"
        try:
            found_servers_count = len([s for s in found_servers if s.get('Status') == 'Found'])
            success_rate = round((found_servers_count / len(found_servers) * 100), 2) if found_servers else 0
            
            summary_data = [
                {'Metric': 'Total Servers Processed', 'Value': len(found_servers)},
                {'Metric': 'Valid Servers Found', 'Value': found_servers_count},
                {'Metric': 'Servers Not Found', 'Value': len(found_servers) - found_servers_count},
                {'Metric': 'Success Rate (%)', 'Value': success_rate},
                {'Metric': 'Total QVL Entries Collected', 'Value': len(all_data)},
                {'Metric': 'TRUSTA Matches Found', 'Value': len([m for m in trusta_matches if m.get('Has_TRUSTA', False)])},
                {'Metric': 'T7P5 Matches Found', 'Value': len([m for m in trusta_matches if m.get('Has_T7P5', False)])},
                {'Metric': 'Total TRUSTA/T7P5 Matches', 'Value': len(trusta_matches)},
                {'Metric': 'Servers with TRUSTA/T7P5', 'Value': len(set([m.get('Server_Model', '') for m in trusta_matches]))},
                {'Metric': 'Completion Date', 'Value': datetime.now().strftime("%Y-%m-%d")},
                {'Metric': 'Completion Time', 'Value': datetime.now().strftime("%H:%M:%S")}
            ]
            
            with open(summary_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Metric', 'Value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in summary_data:
                    writer.writerow(row)
            
            files_created.append(('Summary Statistics', summary_file))
            print(f"? Summary statistics saved to CSV: {summary_file}")
            
        except Exception as e:
            print(f"? Error saving summary CSV: {e}")
        
        print(f"?? Final results saved to {len(files_created)} CSV files")
        return files_created
    
    def test_qvl_detection(self):
        """Test QVL detection on known working URLs - KEEPING ORIGINAL"""
        test_urls = [
            "https://www.gigabyte.com/tw/Enterprise/GPU-Server/G293-S42-AAP1",
            "https://www.gigabyte.com/Enterprise/GPU-Server/G363-ZR0-LAX4-rev-3x"
        ]
        
        if self.driver is None:
            self.setup_selenium_driver()
        
        print("Testing QVL detection on known URLs:")
        print("="*60)
        
        for url in test_urls:
            print(f"\nTesting: {url}")
            try:
                self.driver.get(url)
                time.sleep(3)
                
                page_source = self.driver.page_source
                has_qvl = self.has_qvl(page_source)
                
                print(f"  Page loaded: YES")
                print(f"  Has 'QVL' in content: {'YES' if has_qvl else 'NO'}")
                
                if has_qvl:
                    lines = page_source.split('\n')
                    qvl_lines = [line.strip() for line in lines if 'QVL' in line]
                    print(f"  QVL references found: {len(qvl_lines)}")
                    for i, line in enumerate(qvl_lines[:3]):
                        if line:
                            preview = line[:100] + '...' if len(line) > 100 else line
                            print(f"    {i+1}: {preview}")
                
                if has_qvl:
                    server_model = url.split('/')[-1]
                    print(f"  Testing QVL crawling for: {server_model}")
                    
                    qvl_data = self.crawl_server_qvl(url, server_model)
                    print(f"  QVL entries found: {len(qvl_data)}")
                    
                    if qvl_data:
                        matches = self.search_trusta_in_data(qvl_data)
                        print(f"  TRUSTA/T7P5 matches: {len(matches)}")
                        
                        if matches:
                            for match in matches:
                                print(f"    Match found in server: {match.get('Server_Model')}")
                
            except Exception as e:
                print(f"  Error: {e}")
    
    def run_full_crawl(self, max_servers=None):
        """Run the complete crawling process using sequential flow: detect URL → crawl QVL → next server"""
        
        print("="*80)
        print("GIGABYTE SERVER QVL CRAWLER - SEQUENTIAL FLOW")
        print("Sequential: Detect server URL → If valid, crawl QVL → Move to next server")
        print("="*80)
        
        server_models = self.get_converted_server_list()
        
        if max_servers:
            server_models = server_models[:max_servers]
            print(f"Limited to first {max_servers} servers for testing")
        
        print(f"Total servers to process: {len(server_models)}")
        
        found_servers = []
        all_qvl_data = []
        all_trusta_matches = []
        batch_size = 10
        current_batch_data = []
        batch_files = []
        valid_servers_count = 0
        
        print("\nSEQUENTIAL PROCESSING: Detect → Crawl → Next")
        print("-"*50)
        
        for i, server_model in enumerate(server_models, 1):
            print(f"\n[{i}/{len(server_models)}] Processing: {server_model}")
            
            server_url, category = self.check_server_exists(server_model)
            
            if server_url:
                server_info = {
                    'Server_Model': server_model,
                    'Server_URL': server_url,
                    'Category': category,
                    'Status': 'Found'
                }
                found_servers.append(server_info)
                valid_servers_count += 1
                
                print(f"  ✓ Server found: {server_model}")
                print(f"  → Immediately crawling QVL data...")
                
                qvl_data = self.crawl_server_qvl(server_url, server_model)
                all_qvl_data.extend(qvl_data)
                current_batch_data.extend(qvl_data)
                
                print(f"  ✓ QVL crawling completed: {len(qvl_data)} entries")
                
                if qvl_data:
                    matches = self.search_trusta_in_data(qvl_data)
                    if matches:
                        all_trusta_matches.extend(matches)
                        print(f"  🎯 TRUSTA/T7P5 matches found: {len(matches)}")
                        for match in matches:
                            has_trusta = match.get('Has_TRUSTA', False)
                            has_t7p5 = match.get('Has_T7P5', False)
                            products = []
                            if has_trusta:
                                products.append("TRUSTA")
                            if has_t7p5:
                                products.append("T7P5")
                            print(f"    → {'/'.join(products)} found in {server_model}")
                
            else:
                found_servers.append({
                    'Server_Model': server_model,
                    'Server_URL': '',
                    'Category': '',
                    'Status': 'Not Found'
                })
                print(f"  ✗ Server not found: {server_model}")
            
            # Step 4: Save batch CSV every 10 servers or at the end
            if valid_servers_count > 0 and (valid_servers_count % batch_size == 0 or i == len(server_models)):
                batch_number = (valid_servers_count + batch_size - 1) // batch_size
                total_batches = (len(server_models) + batch_size - 1) // batch_size
                
                if current_batch_data:
                    print(f"\n📊 SAVING CSV BATCH {batch_number}...")
                    print("-"*30)
                    
                    batch_file, batch_matches = self.save_qvl_data_batch_csv(
                        current_batch_data, 
                        batch_number, 
                        total_batches
                    )
                    
                    if batch_file:
                        batch_files.append(batch_file)
                        print(f"  ✓ Batch saved: {batch_file}")
                    
                    current_batch_data = []
            
            print(f"  📈 Progress: {i}/{len(server_models)} servers | {valid_servers_count} valid | {len(all_trusta_matches)} matches")
        
        print(f"\n📋 SEQUENTIAL PROCESSING COMPLETE")
        print("-"*50)
        print(f"Total servers processed: {len(server_models)}")
        print(f"Valid servers found: {valid_servers_count}")
        print(f"Total QVL entries collected: {len(all_qvl_data)}")
        print(f"Total TRUSTA/T7P5 matches found: {len(all_trusta_matches)}")
        
        # Save valid servers list
        print("\n💾 SAVING FINAL CSV FILES...")
        print("-"*40)
        valid_servers_csv = self.save_valid_servers_csv(found_servers)
        
        # Save final consolidated CSV files
        final_csv_files = self.save_final_results_csv(all_qvl_data, all_trusta_matches, found_servers)
        
        # Final summary
        print("\n" + "="*80)
        print("FINAL SUMMARY - SEQUENTIAL FLOW COMPLETED")
        print("="*80)
        print(f"Total servers processed: {len(server_models)}")
        print(f"Valid servers found: {valid_servers_count}")
        print(f"Success rate: {(valid_servers_count/len(server_models)*100):.1f}%")
        print(f"Total QVL entries collected: {len(all_qvl_data)}")
        print(f"TRUSTA/T7P5 matches found: {len(all_trusta_matches)}")
        print(f"CSV batch files created: {len(batch_files)}")
        
        print(f"\n📁 FILES CREATED:")
        print(f"  📊 Valid servers list: {valid_servers_csv}")
        print(f"  📦 QVL data batches: {len(batch_files)} files")
        print(f"  📋 Final consolidated files: {len(final_csv_files)} files")
        for file_type, filename in final_csv_files:
            print(f"    • {file_type}: {filename}")
        
        if all_trusta_matches:
            print(f"\n🎯 TRUSTA/T7P5 MATCHES SUMMARY:")
            print("-"*60)
            
            server_matches = {}
            for match in all_trusta_matches:
                server = match.get('Server_Model', 'Unknown')
                if server not in server_matches:
                    server_matches[server] = {'TRUSTA': 0, 'T7P5': 0}
                if match.get('Has_TRUSTA', False):
                    server_matches[server]['TRUSTA'] += 1
                if match.get('Has_T7P5', False):
                    server_matches[server]['T7P5'] += 1
            
            for i, (server, counts) in enumerate(server_matches.items(), 1):
                print(f"  {i}. {server}:")
                print(f"     TRUSTA matches: {counts['TRUSTA']}")
                print(f"     T7P5 matches: {counts['T7P5']}")
                print(f"     Total matches: {counts['TRUSTA'] + counts['T7P5']}")
        else:
            print("\n❌ No TRUSTA/T7P5 products found in any server QVL")
        
        print(f"\n✅ Sequential crawling completed successfully!")
        print(f"📊 All CSV files saved for detailed analysis")
        
        return found_servers, all_qvl_data, all_trusta_matches
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

def main():
    crawler = GigabyteServerQVLCrawler()
    
    try:
        # First test QVL detection on known URLs
        print("Testing QVL detection functionality...")
        #crawler.test_qvl_detection()
        
        #print("\n" + "="*80)
        #response = input("QVL detection test completed. Press Enter to continue with full crawl, or type 'q' to quit: ")
        #if response.lower() == 'q':
        #    return
        
        # Run full crawl using sequential flow: detect → crawl → next
        found_servers, qvl_data, matches = crawler.run_full_crawl(5)  # Test with 5 servers first
        
        print("\nSequential crawling completed successfully!")
        print("✅ All results saved as CSV files using the new sequential flow")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Error during crawling: {e}")
        import traceback
        traceback.print_exc()
    finally:
        crawler.cleanup()

if __name__ == "__main__":

    main()
