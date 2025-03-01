"""
File processing utilities for handling various file types (PDF, CSV, Excel, etc.).
"""

import os
import pandas as pd
import tempfile
from typing import Dict, Any, List, Tuple, Optional, Union

# File types
class FileType:
    PDF = "pdf"
    CSV = "csv"
    EXCEL = "xlsx"
    TEXT = "txt"
    MARKDOWN = "md"
    
    @staticmethod
    def get_type(file_name: str) -> str:
        """
        Get the file type from its extension.
        
        Args:
            file_name: The name of the file
            
        Returns:
            str: The file type
        """
        extension = file_name.split('.')[-1].lower()
        if extension in ['xls', 'xlsx']:
            return FileType.EXCEL
        elif extension in ['csv']:
            return FileType.CSV
        elif extension in ['pdf']:
            return FileType.PDF
        elif extension in ['txt']:
            return FileType.TEXT
        elif extension in ['md', 'markdown']:
            return FileType.MARKDOWN
        else:
            return extension

class FileProcessor:
    """
    Process various file types for analysis with LLMs.
    """
    
    def __init__(self, uploads_dir: str = None):
        """
        Initialize the file processor.
        
        Args:
            uploads_dir: Directory to store uploaded files
        """
        self.uploads_dir = uploads_dir or os.path.join("app", "data", "uploads")
        os.makedirs(self.uploads_dir, exist_ok=True)
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """
        Save an uploaded file from Streamlit to disk.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            str: Path to the saved file
        """
        # Create a temporary file to store the upload
        temp_dir = self.uploads_dir
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate a unique file path
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Write the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return file_path
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a file based on its type and return relevant content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dict[str, Any]: Processed content and metadata
        """
        file_name = os.path.basename(file_path)
        file_type = FileType.get_type(file_name)
        
        result = {
            "file_name": file_name,
            "file_type": file_type,
            "file_path": file_path,
            "content": None,
            "metadata": {}
        }
        
        # Process based on file type
        if file_type == FileType.CSV:
            content, metadata = self._process_csv(file_path)
            result["content"] = content
            result["metadata"] = metadata
            
        elif file_type == FileType.EXCEL:
            content, metadata = self._process_excel(file_path)
            result["content"] = content
            result["metadata"] = metadata
            
        elif file_type == FileType.PDF:
            content, metadata = self._process_pdf(file_path)
            result["content"] = content
            result["metadata"] = metadata
            
        elif file_type in [FileType.TEXT, FileType.MARKDOWN]:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            result["content"] = text
            result["metadata"] = {"char_count": len(text)}
        
        return result
    
    def _process_csv(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Process a CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Tuple[pd.DataFrame, Dict[str, Any]]: DataFrame and metadata
        """
        df = pd.read_csv(file_path)
        
        metadata = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns)
        }
        
        return df, metadata
    
    def _process_excel(self, file_path: str) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Process an Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]: Dict of DataFrames and metadata
        """
        excel_file = pd.ExcelFile(file_path)
        
        # Read all sheets
        dfs = {}
        for sheet_name in excel_file.sheet_names:
            dfs[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)
        
        metadata = {
            "sheets": excel_file.sheet_names,
            "sheet_count": len(excel_file.sheet_names),
            "sheet_details": {
                sheet: {
                    "rows": len(dfs[sheet]),
                    "columns": len(dfs[sheet].columns),
                    "column_names": list(dfs[sheet].columns)
                }
                for sheet in dfs
            }
        }
        
        return dfs, metadata
    
    def _process_pdf(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Process a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple[str, Dict[str, Any]]: Extracted text and metadata
        """
        try:
            import pypdf
        except ImportError:
            return "PDF processing requires pypdf. Install with: pip install pypdf", {}
        
        # Extract text from PDF
        text = ""
        metadata = {}
        
        try:
            with open(file_path, "rb") as f:
                pdf = pypdf.PdfReader(f)
                metadata = {
                    "pages": len(pdf.pages),
                    "title": pdf.metadata.title if pdf.metadata and pdf.metadata.title else None,
                    "author": pdf.metadata.author if pdf.metadata and pdf.metadata.author else None,
                    "creation_date": pdf.metadata.creation_date if pdf.metadata and pdf.metadata.creation_date else None,
                }
                
                for page_num in range(len(pdf.pages)):
                    page = pdf.pages[page_num]
                    text += page.extract_text() + "\n\n"
                
        except Exception as e:
            return f"Error processing PDF: {str(e)}", {}
        
        return text, metadata
    
    def get_file_summary(self, file_path: str) -> str:
        """
        Generate a summary description of the file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Summary of the file
        """
        result = self.process_file(file_path)
        file_type = result["file_type"]
        
        if file_type == FileType.CSV:
            df = result["content"]
            metadata = result["metadata"]
            return (
                f"CSV file: {result['file_name']}\n"
                f"Rows: {metadata['rows']}, Columns: {metadata['columns']}\n"
                f"Columns: {', '.join(metadata['column_names'])}\n"
                f"Sample data:\n{df.head(5).to_string()}"
            )
            
        elif file_type == FileType.EXCEL:
            dfs = result["content"]
            metadata = result["metadata"]
            summary = [f"Excel file: {result['file_name']}"]
            summary.append(f"Sheets: {', '.join(metadata['sheets'])}")
            
            for sheet_name, sheet_df in dfs.items():
                sheet_info = metadata["sheet_details"][sheet_name]
                summary.append(f"\nSheet: {sheet_name}")
                summary.append(f"Rows: {sheet_info['rows']}, Columns: {sheet_info['columns']}")
                summary.append(f"Columns: {', '.join(sheet_info['column_names'])}")
                summary.append(f"Sample data:\n{sheet_df.head(5).to_string()}")
            
            return "\n".join(summary)
            
        elif file_type == FileType.PDF:
            text = result["content"]
            metadata = result["metadata"]
            return (
                f"PDF file: {result['file_name']}\n"
                f"Pages: {metadata.get('pages', 'Unknown')}\n"
                f"Title: {metadata.get('title', 'Unknown')}\n"
                f"Author: {metadata.get('author', 'Unknown')}\n"
                f"Content preview: {text[:500]}..." if len(text) > 500 else text
            )
            
        elif file_type in [FileType.TEXT, FileType.MARKDOWN]:
            text = result["content"]
            return (
                f"Text file: {result['file_name']}\n"
                f"Size: {result['metadata'].get('char_count', 'Unknown')} characters\n"
                f"Content preview: {text[:500]}..." if len(text) > 500 else text
            )
        
        return f"File: {result['file_name']} (No preview available for {file_type} files)"

# Singleton instance
file_processor = FileProcessor()