from bs4 import BeautifulSoup
import jinja2


class AdditionalFeatures:
    """Class for support additional features related to CanvasJS charts"""

    def __call__(self, template: str, **kwargs) -> str:
        self.soup = BeautifulSoup(template, 'html.parser')
        self.add_canvas_script()
        if "average_capital_allocation_full" in kwargs:
            self.add_average_capital_allocation(kwargs["average_capital_allocation_full"])

        return str(self.soup)

    def add_canvas_script(self):
        """
        Add main CanvasJS script to HEAD section
        """
        canvas_script = self.soup.new_tag("script", src="https://cdn.canvasjs.com/canvasjs.min.js")
        head = self.soup.find("head")
        head.append(canvas_script)

    def add_average_capital_allocation(self, datas):
        """
        Add CanvasJS pie chart with average capital allocation
        """
        def generate_datapoints():
            """
            Generate datapoints used by CanvasJS in format:
            {y: 0.23, label: "SHY"}, {...}
            """
            datapoints = ""
            for ticker, value in datas.items():
                if datapoints:
                    datapoints += ","
                datapoints += f'{{y: {float(value):.4f}, label: "{ticker}"}}'
            return datapoints

        # Get left div, this element contains all charts
        left_div = self.soup.find("div", {"id": "left"})
        # Append new pie chart
        chart_container = self.soup.new_tag("div", id="chartContainer", style="height: 300px; width: 100%;")
        left_div.append(chart_container)

        pie_chart_script = self.soup.new_tag("script")
        template = """window.onload = function() {
            var chart = new CanvasJS.Chart("chartContainer", {
                animationEnabled: false,
                title: {
                    text: "Average Capital Allocation"
                },
                data: [{
                    type: "pie",
                    startAngle: 240,
                    indexLabel: "{label} ({y}%)",
                    yValueFormatString: "##0.00%",
                    indexLabel: "{label} {y}",
                    dataPoints: [
                        {{ data }}
                    ]
                }]
            });
            chart.render();
            }"""
        environment = jinja2.Environment()
        template = environment.from_string(template)
        pie_chart_script.string = template.render(data=generate_datapoints())

        body = self.soup.find("body")
        body.append(pie_chart_script)
