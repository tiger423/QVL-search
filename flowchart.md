# QVL-Search Crawler Flow Diagram

```mermaid
flowchart TD
    A[Start: QVL-Search Crawler] --> B[Initialize GigabyteServerQVLCrawler]
    B --> C[Load Server Models List]
    C --> D[Setup Sequential Processing]
    D --> E[For Each Server Model]
    
    E --> F[Get Category from First Character]
    F --> G{Character Mapping}
    G -->|G| H1[GPU-Server]
    G -->|R| H2[Rack-Server]
    G -->|H| H3[High-Density-Server]
    G -->|S| H4[Storage-Server]
    G -->|X| H5[Rack-Server]
    G -->|E| H6[Rack-Server]
    G -->|Other| H7[General-Purpose-Server]
    
    H1 --> I[Generate Base URL]
    H2 --> I
    H3 --> I
    H4 --> I
    H5 --> I
    H6 --> I
    H7 --> I
    
    I --> J[Test Base URL with Category]
    J --> K{URL Exists & Has QVL?}
    
    K -->|Yes| L[Check for Redirects]
    L --> M[Log Final URL]
    M --> N[Crawl QVL Data]
    
    K -->|No| O[Try Version Suffix: -rev-3x]
    O --> P{URL Exists & Has QVL?}
    P -->|Yes| L
    P -->|No| Q[Try Version Suffix: -rev-1x]
    Q --> R{URL Exists & Has QVL?}
    R -->|Yes| L
    R -->|No| S[Mark Server as Not Found]
    
    N --> T[Extract QVL Table Data]
    T --> U[Search for TRUSTA/T7P5 Matches]
    U --> V[Save QVL Data to Batch]
    V --> W[Update Progress Counters]
    
    S --> W
    W --> X{More Servers?}
    X -->|Yes| E
    X -->|No| Y[Save Final Results]
    
    Y --> Z1[Save Valid Servers CSV]
    Z1 --> Z2[Save QVL Data Batches CSV]
    Z2 --> Z3[Save TRUSTA/T7P5 Matches CSV]
    Z3 --> Z4[Save Summary Statistics CSV]
    Z4 --> AA[End: Display Results Summary]
    
    style A fill:#e1f5fe
    style AA fill:#c8e6c9
    style K fill:#fff3e0
    style P fill:#fff3e0
    style R fill:#fff3e0
    style N fill:#f3e5f5
    style T fill:#f3e5f5
    style U fill:#f3e5f5
```

## Key Features

### Sequential Flow (Ver3+)
- **Detect → Crawl → Next**: Each server is processed individually
- **Immediate Processing**: Valid servers are crawled immediately after detection
- **Efficient Resource Usage**: No need to store large lists in memory

### Smart URL Generation (Ver4)
- **Character-Based Categorization**: Determines server category from first character
- **Redirect Detection**: Logs actual final URL after redirects
- **Version Suffix Fallback**: Tries `-rev-3x` and `-rev-1x` if base URL fails
- **Reduced HTTP Requests**: ~60-70% fewer requests compared to brute-force approach

### Data Processing
- **QVL Table Extraction**: Parses HTML tables from server support pages
- **TRUSTA/T7P5 Detection**: Searches for specific SSD compatibility
- **Batch Processing**: Saves data in manageable chunks
- **Multiple Output Formats**: CSV files for different data types

### Error Handling
- **Selenium WebDriver Management**: Automatic driver setup and cleanup
- **Rate Limiting**: Random delays between requests
- **Exception Handling**: Graceful handling of network and parsing errors
- **Progress Tracking**: Real-time status updates and counters
```
