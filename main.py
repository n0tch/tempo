#!/usr/bin/python
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import json
import requests
import urllib
import os

class Principal():
	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("/home/gustavo/PythonCode/tempo/tela.glade")

		self.janela = builder.get_object("janela")
		self.imagem = builder.get_object("imgDescricao")
		self.cidade = builder.get_object("cidade")
		self.descricao = builder.get_object("descricao")
		self.temperatura = builder.get_object("temperatura")
		self.edtEstado = builder.get_object("edtEstado")
		self.edtCidade = builder.get_object("edtCidade")
		self.infoEstado = builder.get_object("infoEstado")
		self.infoCidade = builder.get_object("infoCidade")
		self.umidade = builder.get_object("umidade")
		###controle para previsoes###
		self.previsao_dia1 = builder.get_object("previsao_dia1")
		self.descricao_dia1 = builder.get_object("descricao_dia1")
		self.max_min_dia1 = builder.get_object("max_min_dia1")
		self.imagem_dia1 = builder.get_object("imagem_dia1")

		self.previsao_dia2 = builder.get_object("previsao_dia2")
		self.descricao_dia2 = builder.get_object("descricao_dia2")
		self.max_min_dia2 = builder.get_object("max_min_dia2")
		self.imagem_dia2 = builder.get_object("imagem_dia2")

		self.previsao_dia3 = builder.get_object("previsao_dia3")
		self.descricao_dia3 = builder.get_object("descricao_dia3")
		self.max_min_dia3 = builder.get_object("max_min_dia3")
		self.imagem_dia3 = builder.get_object("imagem_dia3")

		self.previsao_dia4 = builder.get_object("previsao_dia4")
		self.descricao_dia4 = builder.get_object("descricao_dia4")
		self.max_min_dia4 = builder.get_object("max_min_dia4")
		self.imagem_dia4 = builder.get_object("imagem_dia4")

		self.edtCidade.grab_focus()

		self.conteudo = self.get_json()

		builder.connect_signals({	"on_janela_destroy":self.sair, 
									"on_btnGO_clicked":self.pesquisar})
		self.gtkStyle()
		self.janela.show()

	def sair(self, widget):
		os.remove('imagem_dia.jpg')
		os.remove('imagem_dia1.jpg')
		os.remove('imagem_dia2.jpg')
		os.remove('imagem_dia3.jpg')
		os.remove('imagem_dia4.jpg')
		Gtk.main_quit()

	def gtkStyle(self):
		css = '''
				@import url("css/style.css");
			'''
		self.stylecssprovider = Gtk.CssProvider()
		self.stylecssprovider.load_from_data(css.encode("utf-8"))
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.stylecssprovider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	def popular_controles(self):
		pb = Pixbuf.new_from_file_at_scale("imagem_dia.jpg", width=50, height=50,preserve_aspect_ratio=False)
		self.imagem.set_from_pixbuf(pb)

		self.cidade.set_text(self.conteudo['cidade'])
		self.descricao.set_text(self.conteudo['agora']['descricao'])
		self.temperatura.set_text('Temperatura: ' + self.conteudo['agora']['temperatura'] + ' graus')
		self.umidade.set_text('Umidade: ' + self.conteudo['agora']['umidade'])


		for num, value in enumerate(self.conteudo['previsoes']):
			if num == 1:
				self.previsao_dia1.set_text(value['data'])
				self.descricao_dia1.set_text(value['descricao'])
				img_url = value['imagem']
				response = urllib.request.urlopen(img_url)
				with open("imagem_dia1.jpg", 'wb') as f:
					f.write(response.read())
				pb = Pixbuf.new_from_file_at_scale("imagem_dia1.jpg", width=50, height=50,preserve_aspect_ratio=False)
				self.imagem_dia1.set_from_pixbuf(pb)
				self.max_min_dia1.set_text("Max: " + value['temperatura_max'] + " Min: " + value['temperatura_min'])
			elif num == 2:
				self.previsao_dia2.set_text(value['data'])
				self.descricao_dia2.set_text(value['descricao'])
				img_url = value['imagem']
				response = urllib.request.urlopen(img_url)
				with open("imagem_dia2.jpg", 'wb') as f:
					f.write(response.read())
				pb = Pixbuf.new_from_file_at_scale("imagem_dia2.jpg", width=50, height=50,preserve_aspect_ratio=False)
				self.imagem_dia2.set_from_pixbuf(pb)
				self.max_min_dia2.set_text("Max: " + value['temperatura_max'] + " Min: " + value['temperatura_min'])
			elif num == 3:
				self.previsao_dia3.set_text(value['data'])
				self.descricao_dia3.set_text(value['descricao'])
				img_url = value['imagem']
				response = urllib.request.urlopen(img_url)
				with open("imagem_dia3.jpg", 'wb') as f:
					f.write(response.read())
				pb = Pixbuf.new_from_file_at_scale("imagem_dia3.jpg", width=50, height=50,preserve_aspect_ratio=False)
				self.imagem_dia3.set_from_pixbuf(pb)
				self.max_min_dia3.set_text("Max: " + value['temperatura_max'] + " Min: " + value['temperatura_min'])
			elif num == 4:
				self.previsao_dia4.set_text(value['data'])
				self.descricao_dia4.set_text(value['descricao'])
				img_url = value['imagem']
				response = urllib.request.urlopen(img_url)
				with open("imagem_dia4.jpg", 'wb') as f:
					f.write(response.read())
				pb = Pixbuf.new_from_file_at_scale("imagem_dia4.jpg", width=50, height=50,preserve_aspect_ratio=False)
				self.imagem_dia4.set_from_pixbuf(pb)
				self.max_min_dia4.set_text("Max: " + value['temperatura_max'] + " Min: " + value['temperatura_min'])
	def get_json(self, cidade='', estado=''):
		if cidade:
			dado = requests.get("http://developers.agenciaideias.com.br/tempo/json/{} - {}".format(cidade, estado))
		else:
			dado = requests.get("http://developers.agenciaideias.com.br/tempo/json/sao paulo - SP")

		dado = json.loads(dado.text)
		img_url = dado['agora']['imagem']
		response = urllib.request.urlopen(img_url)
		with open("imagem_dia.jpg", 'wb') as f:
			f.write(response.read())

		self.conteudo = dado
		self.popular_controles()

	def pesquisar(self, widget):
		status = True

		if not self.edtCidade.get_text():
			self.infoCidade.set_text("Informe a cidade!")
			status = False
		else:
			self.infoCidade.set_text("")

		if not self.edtEstado.get_text():
			self.infoEstado.set_text("Informe o estado!")
			status = False
		else:
			self.infoEstado.set_text("")

		if status:
			print("Paramentros preenchidos!")
			self.get_json(self.edtCidade.get_text(), self.edtEstado.get_text())
		else:
			print("Status = False.")



if __name__ == '__main__':
	app = Principal()
	Gtk.main()