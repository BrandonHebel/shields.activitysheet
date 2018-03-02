from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from io import BytesIO
import calendar

from .secrets import HR_EMAIL

def generate_pdf(request, activitysheet):
	buffer1 = BytesIO()
	title = 'Timesheet - {} - {} - {}'.format(request.user.username,
		activitysheet.date.strftime('%x'),
		calendar.day_name[activitysheet.date.weekday()]
	)
	doc = SimpleDocTemplate(
		buffer1,
		title=title,
		author=request.user.username,
		pagesize=A4,
		rightMargin=30,leftMargin=30,
		topMargin=30,
		bottomMargin=18,
	)
	doc.pagesize = portrait(A4)
	elements = []

	# Generate table data
	data = [['', 'Start Time', 'End Time', 'Total Time']]
	activities = activitysheet.activity_set.all()
	for activity in activities:
		data.append([
			activity.name,
			activity.start_time.strftime('%I:%M %p'),
			activity.end_time.strftime('%I:%M %p'),
			str(activity.total_time) + " hrs"
		])

	# Configure style and word wrap
	style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])

	s = getSampleStyleSheet()
	style_body_text = s["BodyText"]
	style_body_text.wordWrap = 'CJK'
	style_heading = s['Heading1']

	# Build the data
	elements.append(Paragraph(title, style_heading))
	elements.append(Spacer(0, 0.1*inch))
	data2 = [[Paragraph(cell, style_body_text) for cell in row] for row in data]
	t=Table(data2)
	t.setStyle(style)
	elements.append(t)
	elements.append(Spacer(0, 0.1*inch))
	elements.append(Paragraph(str(activitysheet.total_time) + " hrs Total", style_heading))
	doc.build(elements)
	pdf = buffer1.getvalue()
	buffer1.close()
	return pdf


def send_pdf(request, activitysheet):
	pdf = generate_pdf(request, activitysheet)
	date = activitysheet.date.strftime('%m-%d-%Y')
	title = 'Timesheet - {} {}'.format(request.user.username, date)
	content = '{} - Total Hours: {}'.format(request.user.username, activitysheet.total_time)
	print("HR_EMAIL: " + HR_EMAIL)
	msg = EmailMessage(title, content, 'webservice@brandonhebel.com', [request.user.email, HR_EMAIL])
	msg.attach('Timesheet_{}_{}.pdf'.format(request.user.username, date), pdf, 'application/pdf')
	msg.content_subtype = "html"
	msg.send()


def view_pdf(request, activitysheet):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Timesheet_{}_{}.pdf"'.format(
		request.user.username, activitysheet.date.strftime('%m.%d.%Y')
	)
    response.write(generate_pdf(request, activitysheet))
    return response
