#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright 2012 Quequeré
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------

from contantes import *
from random import choice, randint


class Efeito(object):
    exp = "^Nada acontece$"
    @classmethod
    def descer(cls, dados, dono, carta):
        pass
    @classmethod
    def perder(cls, dono, carta):
        pass

class Permanente(object):
    @classmethod
    def descer(cls, dados, dono, carta):
        dono.adi_especial(cls.especial, carta)
    @classmethod
    def perder(cls, dono, carta):
        dono.rem_especial(cls.especial, carta)


class DinheiroMaioria(Efeito):
    exp = "^Jogador que tiver mais cartas (?P<tipo>\w+) (?P<naipe>\w+) baixadas na mesa (?P<acao>\w+) (?P<quant>\w+)\$$"
    @classmethod
    def descer(cls, dados, dono, carta):
        """Da dinheiro para jogador com uma determinada maioria"""
        nome_jog = dono.jogo.maiorias.get(dados["naipe"].lower())
        if nome_jog != None:
            if dados["acao"] == "perde":
                sinal = -1
            else:
                sinal = 1
            nomes = nome_jog[1]
            for nome in nomes:
                jog = dono.jogo.jogadores[nome]
                alteracao = int(sinal*int(dados["quant"])/len(nomes))
                jog.dinheiro += alteracao

class AlterarDinheiro(Efeito):
    exp = "^(?P<acao>\w+) (?P<quant>\w+)\$$"
    @classmethod
    def descer(cls, dados, dono, carta):
        """Altera a quantidade de dinheiro do dono da carta"""
        if dados["acao"] == "perde":
            sinal = -1
        else:
            sinal = 1
        alteracao = int(sinal*int(dados["quant"]))
        dono.dinheiro += alteracao

class JogadorComMaisDinheiro(Efeito):
    exp = "^Caso seja o jogador com mais dinheiro, (?P<acao>\w+) (?P<quant>\w+)\$$"
    @classmethod
    def descer(cls, dados, dono, carta):
        """Altera a quantidade de dinheiro do dono da carta"""
        if dono.dinheiro == dono.jogo.ret_jog_mais_dinheiro().dinheiro:
            if dados["acao"] == "perde":
                sinal = -1
            else:
                sinal = 1
            alteracao = int(sinal*int(dados["quant"]))
            dono.dinheiro += alteracao

class RecebeCartasMonte(Efeito):
    exp = "^Recebe (?P<quant>\w+) cartas do monte$"
    @classmethod
    def descer(cls, dados, dono, carta):
        """Dono da carta pega X cartas do monte"""
        for i in range(int(dados["quant"])):
            if len(dono.mao) < MAX_CARTAS_MAO:
                carta = dono.jogo.pegar_carta_monte()
                if carta != None:
                    dono.adi_carta(carta)

class VantagemEmpateNaipe(Permanente, Efeito):
    exp = "^Vantagem na maioria em caso de empate de cartas deste naipe$"
    especial = "calculo_maioria"
    @classmethod
    def executar(cls, dados, dono, carta):
        if dados["naipe"] == carta.naipe:
            dados["quant"] += 0.5

class RecebeDinheiroPorMaiorias(Efeito):
    exp = "^Recebe (?P<quant>\w+)\$ pra cada naipe que tiver maioria na mesa$"
    @classmethod
    def descer(cls, dados, dono, carta):
        dono.dinheiro += int(carta.efeito_dados["quant"]) * len(dono.maiorias)

class RecebeNaipesDiferentes(Efeito):
    exp = "^Recebe (?P<quant>\w+)\$ para cada 2 naipes diferentes que tiver cartas na mesa$"
    @classmethod
    def descer(cls, dados, dono, carta):
        dono.dinheiro += int(carta.efeito_dados["quant"]) * int(len(dono.mesa)/2)

class ExcluiAleatoriamenteCartasDosOutros(Efeito):
    exp = "^O jogador exclui aleatoriamente uma carta na m\wo de todos os outros jogadores$"
    @classmethod
    def descer(cls, dados, dono, carta):
        for j in dono.jogo.jogadores.values():
            if j != dono:
                escolha = choice(j.mao)
                if escolha:
                    j.mao.remove(escolha)

class DinheiroMoeda(Efeito):
    exp = "^Joga uma moeda, escolhe cara ou coroa, se acertar ganha (?P<quant1>\w+)\$, se errar perde (?P<quant2>\w+)\$$"
    @classmethod
    def descer(cls, dados, dono, carta):
        moeda = randint(0, 1)
        if moeda:
            dono.dinheiro += int(carta.efeito_dados["quant1"])
        else:
            dono.dinheiro -= int(carta.efeito_dados["quant2"])
        if dono.dinheiro < 0:
            dono.dinheiro = 0

class DinheiroDado(Efeito):
    exp = "^Joga-se um dado, o jogador ganha dinheiro equivalente a (?P<quant>\w+) vezes o valor, caso saia 6 n\wo ganha nada$"
    @classmethod
    def descer(cls, dados, dono, carta):
        dado = randint(1, 6)
        if dado != 6:
            dono.dinheiro += int(carta.efeito_dados["quant"]) * dado

class OutrosPerdemDinheiro(Efeito):
    exp = "^Caso tenha (?P<quant>\w+) pts a mais do que qualquer um dos demais jogadores, o jogo termina e voc\w vence$"
    @classmethod
    def descer(cls, dados, dono, carta):
        vencer = True
        for j in dono.jogo.jogadores.values():
            if j != dono and (dono.pontos-j.pontos) < carta.efeito_dados["quant"]:
                vencer = False
        if vencer:
            dono.jogo.fim = True

class OutrosPerdemDinheiro(Efeito):
    exp = "^Todos os demais jogadores perdem todo seu dinheiro$"
    @classmethod
    def descer(cls, dados, dono, carta):
        for j in dono.jogo.jogadores.values():
            if j != dono:
                j.dinheiro = 0

class PontosPorCartaFinal(Permanente, Efeito):
    exp = "^Jogador recebe (?P<quant>\w+) ponto\w? por carta (?P<tipo>\w+) (?P<naipe>\w+) ao final do jogo$"
    especial = "calculo_pontos_finais"
    @classmethod
    def executar(cls, dados, dono, carta):
        naipe = carta.efeito_dados["naipe"].lower()
        num = len(dono.mesa[naipe])
        dados["pontos"] += int(carta.efeito_dados["quant"]) * num

class PontosFinal(Permanente, Efeito):
    exp = "^A carta vale mais (?P<quant>\w+) ponto\w? ao final do jogo$"
    especial = "calculo_pontos_finais"
    @classmethod
    def executar(cls, dados, dono, carta):
        dados["pontos"] += int(carta.efeito_dados["quant"])

class DinheiroAoBaixar(Permanente, Efeito):
    exp = "^Jogador ganha \+(?P<quant1>\w+)\$ ao baixar carta (?P<tipo>\w+) de (?P<naipe>\w+) de valor 1,3,5 e \+(?P<quant2>\w+)\$ de valor 7 e 9$"
    especial = "ao_descer_carta"
    @classmethod
    def executar(cls, dados, dono, carta):
        carta_baixada = dados["carta"]
        if carta_baixada.naipe == carta.efeito_dados["naipe"].lower():
            if carta_baixada.valor in [1, 3, 5]:
                dados["dinheiro"] += int(carta.efeito_dados["quant1"])
            elif carta_baixada.valor in [7, 9]:
                dados["dinheiro"] += int(carta.efeito_dados["quant2"])

class ReceberMaisDinheiro(Permanente, Efeito):
    exp = "^PODER FIXO: quando escolher receber dinheiro, recebe (?P<quant>\w+)\$ a mais$"
    especial = "ao_pegar_dinheiro"
    @classmethod
    def executar(cls, dados, dono, carta):
        dados["dinheiro"] += int(carta.efeito_dados["quant"])
