import json
from xml.dom import minidom
from flask_socketio import SocketIO

def sflash(dest, msg, button=True, redir=None):
		doc = minidom.Document()
		flash = doc.createElement("div")
		flash.setAttribute("class", "alert alert-danger alert-dismissable")
		flash.setAttribute("style", "z-index: 1;")
		doc.appendChild(flash)

		m_text = doc.createTextNode(f"{msg}")
		flash.appendChild(m_text)

		if button or redir:
			br = doc.createElement("br")
			flash.appendChild(br)

			btn_box = doc.createElement("div")
			flash.appendChild(btn_box)

		if button:
			
			btn = doc.createElement("button")
			btn.setAttribute("type", "button")
			btn.setAttribute("class", "btn btn-secondary")
			btn.setAttribute("data-bs-dismiss", "alert")
			btn.setAttribute("aria-label", "Close")

			btn_span = doc.createElement("span")
			btn_span_txt = doc.createTextNode("OK")
			btn_span.setAttribute("aria-hidden", "true")

			
			btn_box.appendChild(btn)
			btn.appendChild(btn_span)
			btn_span.appendChild(btn_span_txt)

		if redir:
			redir_btn = doc.createElement("a")
			redir_btn.setAttribute("class", "btn btn-secondary")
			redir_btn.setAttribute('href', 'javascript:void(0)')
			redir_btn.setAttribute('onclick', f'window.location.href = "http://" + window.location.host + "{redir}"')
			redir_btn.setAttribute("target", "_self")

			redir_btn_span = doc.createElement("span")
			redir_btn_span_txt = doc.createTextNode("Mission Control")

			btn_box.appendChild(redir_btn)
			redir_btn.appendChild(redir_btn_span)
			redir_btn_span.appendChild(redir_btn_span_txt)

		message = doc.toprettyxml(indent="  ")

		response = json.dumps({
			"dest": dest,
			"HTML": message
			})

		return response