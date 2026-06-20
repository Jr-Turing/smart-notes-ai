import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageTemplate, Frame, PageBreak
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from datetime import datetime


class FooterCanvas(canvas.Canvas):
    """Custom canvas with header and footer"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.page_num = 0
    
    def showPage(self):
        self.page_num += 1
        self._drawFooter()
        canvas.Canvas.showPage(self)
    
    def _drawFooter(self):
        """Draw footer with page number and author"""
        # Save current state
        self.saveState()
        
        # Set font for footer
        self.setFont("Courier-Oblique", 9)
        self.setFillColor(HexColor("#666666"))
        
        # Draw footer line
        self.setLineWidth(0.5)
        self.setStrokeColor(HexColor("#CCCCCC"))
        self.line(0.75*inch, 0.5*inch, 7.75*inch, 0.5*inch)
        
        # Left side - author
        self.drawString(0.75*inch, 0.3*inch, "by curious arvind")
        
        # Right side - page number
        page_text = f"page {self.page_num}"
        self.drawRightString(7.75*inch, 0.3*inch, page_text)
        
        # Restore state
        self.restoreState()


def _make_rich_text(text):
    """Convert markdown-like bold markers (**text**) to bold formatting"""
    # This function will be used during paragraph creation
    return text


def _parse_and_format_text(text):
    """Parse text and convert ** markers to <b> tags for RichText support"""
    # Replace **text** with <b>text</b> for bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    return text


def _is_important_point(line):
    """Identify if a line is an important point based on patterns"""
    line_lower = line.strip().lower()
    
    # Patterns that indicate important points
    important_markers = [
        'important:',
        'note:',
        'key point:',
        'definition:',
        'formula:',
        'remember:',
        'tip:',
        'rule:',
        'concept:'
    ]
    
    # Check if line starts with any important marker
    for marker in important_markers:
        if line_lower.startswith(marker):
            return True
    
    # Check if line contains numbers and key terms (likely important)
    if any(marker in line_lower for marker in ['law of', 'theorem', 'principle', 'equation', 'method']):
        return True
    
    return False


def create_pdf(content, filename, subject, topic):
    """
    Create a professional PDF with handwritten style font, footer, and bold important points
    
    Args:
        content: The markdown content to convert to PDF
        filename: Output PDF filename
        subject: The subject name for the title
        topic: The topic name for the title
    """
    
    # Create PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Custom styles for professional handwritten look
    styles = getSampleStyleSheet()
    
    # Title style - using Courier for monospace handwritten look
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='Courier-BoldOblique',
        fontSize=24,
        textColor=HexColor("#1a1a1a"),
        spaceAfter=12,
        alignment=1,  # Center alignment
        leading=28,
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName='Courier-Bold',
        fontSize=14,
        textColor=HexColor("#2c3e50"),
        spaceAfter=8,
        spaceBefore=10,
        leading=16,
    )
    
    # Body style with handwritten feel
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName='Courier',
        fontSize=11,
        textColor=HexColor("#333333"),
        spaceAfter=8,
        leading=14,
        alignment=4,  # Justify alignment
    )
    
    # Important point style (bold)
    important_style = ParagraphStyle(
        'ImportantPoint',
        parent=styles['BodyText'],
        fontName='Courier-Bold',
        fontSize=11,
        textColor=HexColor("#c0392b"),  # Red color for important
        spaceAfter=8,
        spaceBefore=6,
        leading=14,
        alignment=4,
    )
    
    # Add title
    full_title = f"{subject} - {topic}"
    elements.append(Paragraph(full_title.upper(), title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Add timestamp
    timestamp = datetime.now().strftime("%B %d, %Y")
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontName='Courier-Oblique',
        fontSize=9,
        textColor=HexColor("#999999"),
        alignment=1,
    )
    elements.append(Paragraph(timestamp, date_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Parse content
    lines = content.split('\n')
    
    current_section = None
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines but add minimal space
        if not stripped:
            elements.append(Spacer(1, 0.05*inch))
            continue
        
        # Heading detection (markdown style # or ##)
        if stripped.startswith('###'):
            section_text = stripped.lstrip('#').strip()
            elements.append(Paragraph(section_text, heading_style))
            current_section = section_text
            
        elif stripped.startswith('##'):
            section_text = stripped.lstrip('#').strip()
            elements.append(Paragraph(section_text, heading_style))
            current_section = section_text
            
        elif stripped.startswith('#'):
            section_text = stripped.lstrip('#').strip()
            elements.append(Paragraph(section_text, heading_style))
            current_section = section_text
        
        # Bullet points
        elif stripped.startswith('-') or stripped.startswith('•'):
            bullet_text = stripped.lstrip('-•').strip()
            
            # Check if it's an important point
            if _is_important_point(bullet_text) or any(word in bullet_text.lower() for word in ['important', 'must', 'always', 'never', 'essential']):
                formatted_text = _parse_and_format_text(bullet_text)
                elements.append(Paragraph(f"<b>• {formatted_text}</b>", important_style))
            else:
                formatted_text = _parse_and_format_text(bullet_text)
                elements.append(Paragraph(f"• {formatted_text}", body_style))
        
        # Numbered points
        elif re.match(r'^\d+\.', stripped):
            number_match = re.match(r'^(\d+\.)\s*(.*)', stripped)
            if number_match:
                number = number_match.group(1)
                text = number_match.group(2)
                
                if _is_important_point(text) or any(word in text.lower() for word in ['important', 'must', 'always', 'never', 'essential']):
                    formatted_text = _parse_and_format_text(text)
                    elements.append(Paragraph(f"<b>{number} {formatted_text}</b>", important_style))
                else:
                    formatted_text = _parse_and_format_text(text)
                    elements.append(Paragraph(f"{number} {formatted_text}", body_style))
        
        # Regular paragraphs
        else:
            formatted_text = _parse_and_format_text(stripped)
            
            # Auto-detect important points
            if _is_important_point(stripped) or any(word in stripped.lower() for word in ['important', 'must', 'always', 'never', 'essential', 'note:', 'key']):
                elements.append(Paragraph(f"<b>{formatted_text}</b>", important_style))
            else:
                elements.append(Paragraph(formatted_text, body_style))
    
    # Build PDF with custom canvas
    doc.build(elements, canvasmaker=FooterCanvas)
    
    print(f"PDF created successfully: {filename}")
