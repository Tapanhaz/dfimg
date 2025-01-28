# -*- coding: utf-8 -*-
"""
    :description: Pandas / Polars Dataframe to image.
    :author: Tapan Hazarika
    :created: On Sunday Jan 26, 2025 16:00:39 GMT+05:30
"""
__author__ = "Tapan Hazarika"

import base64
import platform
import requests
import polars as pl
import pandas as pd
from io import BytesIO
from typing import Literal
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

BG_COLOR = "white"
COLOR = "black"

if platform.system() == "Windows" or platform.system() == "Darwin":
    FONT = "arial.ttf"
else:
    FONT = "DejaVuSans.ttf"

FONT_WEIGHT = "normal"
BORDER_COLOR = "black"
COL_DATA_TYPES = ["String", "Int", "Float", "Boolean", "Datetime", "Date", "Time"]

stroke_width = {
    "normal": 0.10,
    "bold": 0.15,
    "bolder": 0.20,
    "lighter": 0.05
}

def get_html_table(
        data: pl.DataFrame,
        table_formatting: str,
        float_precision: int,
        thousands_separator: str
        )-> str:
    row_len, col_len = data.shape
    with pl.Config(
        ascii_tables= True,
        set_tbl_formatting= table_formatting,
        float_precision= float_precision,
        thousands_separator= thousands_separator,
        tbl_rows= row_len,
        tbl_cols= col_len,
        tbl_hide_dataframe_shape= True,
        tbl_hide_column_data_types= True,
    ):
        return data._repr_html_()

def extract_style(tag):
    style = {}
    if tag.get('style'):
        styles = tag['style'].split(';')
        for s in styles:
            if s.strip():
                prop, value = s.split(':')
                style[prop.strip()] = value.strip()
    return style

def df_to_html_img(
        dataframe: pl.DataFrame | pd.DataFrame, 
        title: str= "",
        image_title_font: str= None,
        image_table_font: str= None,
        image_title_font_size: str= 16,
        image_table_font_size: str= 12,
        image_cells_border_color: str= None,
        style: dict= {"bg-color": "white", "color": "black", "font-weight": "normal"},
        tbl_style: dict= {"bg-color": "white", "color": "black", "font-weight": "normal"},
        header_style: dict= {"bg-color": "DarkViolet", "color": "white", "font-weight": "bold"},
        highlight_conditions: dict= {},
        column_style: dict= {},
        content_based_style: dict= {},
        table_formatting: Literal[
                                "ASCII_FULL", "ASCII_FULL_CONDENSED", "ASCII_NO_BORDERS", "ASCII_BORDERS_ONLY", 
                                "ASCII_BORDERS_ONLY_CONDENSED", "ASCII_HORIZONTAL_ONLY", "ASCII_MARKDOWN", 
                                "MARKDOWN", "NOTHING"
                                ]= "ASCII_MARKDOWN",
        cell_padding: int= 10, 
        min_cell_width: int=100, 
        float_precision: int= 2,
        thousands_separator: str= "_",
        return_type: Literal["html", "pil_image"]= "pil_image"
        ):
    dtype_list: list= []
    
    if isinstance(dataframe, pd.DataFrame):
        dataframe = pl.from_pandas(dataframe)
    if not isinstance(dataframe, pl.DataFrame):
        raise TypeError("Input dataframe type is not supported.")
    
    data_types: list= dataframe.dtypes

    for idx, dtype in enumerate(data_types):
        for i in COL_DATA_TYPES:
            if str(dtype).__contains__(i):
                dtype_list.append(i)
                break
        if len(dtype_list) != len(data_types[:idx+1]):
            dtype_list.append("Others")

    html_data = get_html_table(
                        dataframe, 
                        table_formatting= table_formatting,
                        float_precision= float_precision, 
                        thousands_separator= thousands_separator
                        )
    html_data = html_data.replace('&quot;', '')
    
    soup = BeautifulSoup(html_data, "lxml")
    soup.body["style"] = f'''
                        background-color: {style.get("bg-color", BG_COLOR)}; 
                        color: {style.get("color", COLOR)}
                        '''

    table = soup.find("table", class_="dataframe")
    table["style"] = "table-layout: auto;"

    headers = soup.find_all("th")
    all_rows = soup.find_all("tr")
    rows = all_rows[1:]

    for header in headers:
        header["style"] = f'''
                            background-color: {header_style.get('bg-color', BG_COLOR)}; 
                            color: {header_style.get('color', COLOR)};
                            font-weight: {header_style.get("font-weight", FONT_WEIGHT)}
                            '''

    for row in rows:
        cells = row.find_all("td")
        for idx, cell in enumerate(cells):
            col_data_type = dtype_list[idx]
            col_header = headers[idx].text.strip()
            cell_bg_color = None
            cell_font_color = None
            if column_style:
                col_style = column_style.get(col_header)
                if col_style:                
                    cell_bg_color = col_style.get("bg-color", BG_COLOR)
                    cell_font_color = col_style.get("color", COLOR)
                    cell_font_weight = col_style.get("font-weight", FONT_WEIGHT)  
            elif content_based_style: 
                col_style = content_based_style.get(col_data_type)
                if col_style:                
                    cell_bg_color = col_style.get("bg-color", BG_COLOR)
                    cell_font_color = col_style.get("color", COLOR)
                    cell_font_weight = col_style.get("font-weight", FONT_WEIGHT)          
            if highlight_conditions:
                col_condition = highlight_conditions.get(col_header)
                if col_condition:
                    condition = col_condition["condition"]
                    cell_content = cell.text.strip()
                    if col_data_type == "Boolean":
                        if eval(cell_content.capitalize()) == condition:
                            cell_bg_color = col_condition.get("bg-color", BG_COLOR)
                            cell_font_color = col_condition.get("color", COLOR)
                            cell_font_weight = col_condition.get("font-weight", FONT_WEIGHT)
                    elif col_data_type == "String":
                        if eval(f"'{cell_content}'{condition}"):
                            cell_bg_color = col_condition.get("bg-color", BG_COLOR)
                            cell_font_color = col_condition.get("color", COLOR)
                            cell_font_weight = col_condition.get("font-weight", FONT_WEIGHT)
                    elif eval(f"{cell_content}{condition}"):
                        cell_bg_color = col_condition.get("bg-color", BG_COLOR)
                        cell_font_color = col_condition.get("color", COLOR)
                        cell_font_weight = col_condition.get("font-weight", FONT_WEIGHT)
            if not cell_bg_color:
                cell_bg_color = tbl_style.get("bg-color", BG_COLOR)
                cell_font_color = tbl_style.get("color", COLOR)  
                cell_font_weight = tbl_style.get("font-weight", FONT_WEIGHT)          
            cell["style"] = f'''
                            background-color: {cell_bg_color}; 
                            color: {cell_font_color};
                            font-weight: {cell_font_weight}
                            '''
    #print(soup)
    if return_type == "html":
        return str(soup)
    
    try:
        title_font = ImageFont.truetype(image_title_font or FONT, image_title_font_size)
        table_font = ImageFont.truetype(image_table_font or FONT, image_table_font_size)
    except:
        title_font = ImageFont.load_default()
        table_font = ImageFont.load_default()
    
    all_cells: list= []
    for row in all_rows:
        cells = row.find_all(['th', 'td'])
        all_cells.append([cell.text.strip() for cell in cells])
    
    #print(all_cells)
    col_widths = [
            max(
                min_cell_width, 
                max(table_font.getbbox(str(cells[i]))[2] + (cell_padding * 2) 
                    for cells in all_cells)
                ) for i in range(len(all_cells[0])
            )
        ]
    #print(col_widths)

    row_height = max(
                    table_font.getbbox(
                            str(cell))[3] for row in all_cells for cell in row
                            ) + (cell_padding * 2)
    total_width = max(sum(col_widths), title_font.getbbox(title)[2] + (cell_padding * 2))

    title_height = title_font.getbbox(title)[3] + (cell_padding * 2) if title else 0
    total_height = len(all_cells) * row_height + title_height

    img = Image.new(
                mode= 'RGB', 
                size= (total_width, total_height), 
                color= style.get("bg-color", BG_COLOR)
                )
    draw = ImageDraw.Draw(img)

    if title is not None:
        text_width = title_font.getbbox(title)[2]
        text_x = (total_width - text_width) // 2
        draw.text((text_x, cell_padding), title, fill='black', font=title_font)

    y_pos = title_height
    for row in all_rows:
        x_pos = 0
        cells = row.find_all(['th', 'td'])
        for col_idx, cell in enumerate(cells):
            content = cell.text.strip() 
            style = extract_style(cell)
            bg_color = style.get('background-color', BG_COLOR)
            text_color = style.get('color', COLOR)
            font_weight = style.get('font-weight', FONT_WEIGHT)

            draw.rectangle(
                xy= [(x_pos, y_pos), (x_pos + col_widths[col_idx], y_pos + row_height)],
                fill=bg_color,
                outline= image_cells_border_color or BORDER_COLOR
            )
            
            text_width = table_font.getbbox(str(content))[2]
            text_x = x_pos + (col_widths[col_idx] - text_width) // 2
            text_y = y_pos + (row_height - table_font.getbbox(str(content))[3]) // 2
            draw.text(
                xy= (text_x, text_y), 
                text= str(content), 
                fill=text_color, 
                font=table_font,
                stroke_width= stroke_width.get(font_weight, 0),
                stroke_fill= text_color
                )
            
            x_pos += col_widths[col_idx]
        y_pos += row_height
    return img

def image_to_bin(
        img: Image, 
        format: str= "PNG"
        )-> bytes:
    buf = BytesIO()
    img.save(buf, format=format)
    img_str = base64.b64encode(buf.getvalue()).decode()    
    img_base64 = f"data:image/{format.lower()};base64,{img_str}"
    base64_str = img_base64.split(',')[1]
    img_bin = base64.b64decode(base64_str)
    return img_bin

def send_img_to_telegram(
            img: Image,
            chat_id: str,
            bot_token: str,
            img_name: str= "sample",
            format: str= "PNG"
            )-> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    img_bin = image_to_bin(img= img, format= format)
    files = {
            "photo": (
                f"{img_name}.{format.lower()}", 
                img_bin, 
                f"image/{format.lower()}"
                )
            }
        
    data = {
        "chat_id": chat_id,
        "parse_mode": "HTML"
    }

    res = requests.post(url, files=files, data=data)
    if res.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code:: {res.status_code} :: {res.text}")