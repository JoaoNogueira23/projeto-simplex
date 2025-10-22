# Projeto Simplex

## 📘 Descrição

Este projeto implementa o **método Simplex**, utilizado em **Programação Linear (Pesquisa Operacional)** para resolver problemas de **otimização** (maximização ou minimização de funções lineares sujeitas a restrições lineares).

O objetivo é permitir que estudantes e profissionais possam compreender e aplicar o método de forma prática, visualizando cada etapa do processo de iteração até a obtenção da solução ótima.

---

## ⚙️ Funcionalidades

* Definição da **função objetivo** (Max ou Min).
* Inserção das **restrições lineares**.
* Execução automática do **método Simplex** passo a passo.
* Exibição da **solução ótima** (ou indicação de que o problema é inviável ou ilimitado).
* Estrutura modular e clara, fácil de expandir e adaptar para novos casos.

---

## 🧠 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Biblioteca principal:** NumPy
* **Estilo:** Código estruturado e comentado para fins didáticos
* **Licença:** [CC0 1.0 (Domínio Público)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/JoaoNogueira23/projeto-simplex.git
cd projeto-simplex
```

### 2. (Opcional) Crie um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Instale dependências (se houver)

```bash
pip install -r requirements.txt
```

### 4. Execute o script principal

```bash
python SimplexMethod.py
```

---

## 🧮 Exemplo de Uso

**Problema:**
Maximizar

> z = 3x₁ + 5x₂

Sujeito a:

> x₁ + 2x₂ ≤ 4
> 3x₁ + x₂ ≤ 5
> x₁, x₂ ≥ 0

**Saída esperada:**

> x₁ = 1
> x₂ = 1.5
> z = 10.5

---

## 💡 Melhorias Futuras

* Adicionar **interface gráfica (GUI)** com Tkinter ou Streamlit.
* Permitir **entrada de dados via arquivo (JSON ou CSV)**.
* Implementar **fase 2** do método Simplex.
* Exportar resultados em PDF ou Excel.
* Adicionar **testes automatizados** (pytest).

---

## 🤝 Contribuições

Sinta-se à vontade para abrir **issues** e enviar **pull requests** com melhorias!
Mantenha um código limpo, bem comentado e com exemplos claros.

---

## 📄 Licença

Este projeto está sob a licença **CC0 1.0 (Domínio Público)** — você pode usar, modificar e distribuir livremente.

---

## 👤 Autor

**João Victor Nogueira Martins**
📎 [GitHub](https://github.com/JoaoNogueira23)
💬 Aberto a sugestões e colaborações!
