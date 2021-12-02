import os

from fpdf import FPDF, HTMLMixin
import plotly

from solution.cvrp.route import RouteCvrp
from solution.cvrp.solution import SolutionCvrp

class PDF(FPDF, HTMLMixin):
    def header(self):
        """
        """

        # Logo
        self.set_xy(6.0,6.0)
        self.image('./gui/static/image/logo_utbm_no_bg.png', link='', type='', w=19, h=21)

    # Page footer
    def footer(self):
        """
        """

        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def route(self, solution: SolutionCvrp):
        """
        """
        
        # Set the routes
        # Line break
        self.ln(10)
        self.cell(w=0.0, h=40.0, align='L', txt="Routes:", border=0)
        # Line break
        self.ln(30)

        self.set_font("Arial", size=12)
        
        col_width = [self.w * 0.15, self.w * 0.70, self.w * 0.1]
        row_height = self.font_size

        # Set the header row
        self.cell(col_width[0], row_height, txt=f"Route", border=1)
        self.cell(col_width[1], row_height, txt="Customers", border=1)
        self.cell(col_width[2], row_height, txt="Cost", border=1)
        self.ln(row_height)

        for index, route in enumerate(solution.route):
            self.cell(col_width[0], row_height, txt=f"Route #{index+1}", border=1)
            self.cell(col_width[1], row_height, txt=str(route), border=1)
            self.cell(col_width[2], row_height, txt=str(round(route.evaluation())), border=1)
            self.ln(row_height)
            
    def globalInformation(self, algorithm_name: str, min_cost: float):
        """
        """
        self.set_font('Helvetica', '', 15)

        self.cell(w=0.0, h=20.0, align='C', txt="CVRP Report", border=0)
        # Line break
        self.ln(5)
        self.line(5.0,30.0,205.0,30.0)
        self.ln(5)
        # Set the best algorithm name
        self.cell(w=0.0, h=40.0, align='L', txt=f"Best algorithm: {algorithm_name}", border=0)
        # Line break
        self.ln(5)
        # Set the best algotrithm cost
        self.cell(w=0.0, h=40.0, align='L', txt=f"Best solution cost: {min_cost}", border=0)


def createPDF(algorithm_name: str, min_cost: float, solution: str, name: str):
    """
    Function to create a pdf
    """

    pdf = PDF()
    pdf.alias_nb_pages()
    
    pdf.add_page()
    pdf.globalInformation(algorithm_name=algorithm_name, min_cost=min_cost)
    pdf.route(solution=solution)
    
    pdf.add_page(orientation="L")
    image_path = name[:-3] + "png"
    plotly.io.write_image(solution.getFigurePlotly(), file=image_path, format='png')
    pltx=(image_path)
    pdf.image(pltx)
    
    pdf.output(name, 'F')

