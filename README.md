# dfimg
Convert polars / pandas dataframe to image/ binary image. 

## Installation ::

For intallation use pip :

```shell
pip install dfimg
```

## Functions ::

dfimg provides the following functions:

df_to_html_img:
    This function performs the main task of converting a Polars or Pandas DataFrame to an HTML or PIL image.

    Parameters:
        dataframe (required): The Polars or Pandas DataFrame to be converted.
        title (optional): Title string to display on top of the image. Default is an empty string.
        image_title_font (optional): Font to be used for the title. Default is None.
        image_table_font (optional): Font for the table content. Default is None.
        image_title_font_size (optional): Font size for the title. Default is 16.
        image_table_font_size (optional): Font size for the table content. Default is 12.
        image_cells_border_color (optional): Color for cell borders. Default is None.
        style (optional): Styles for the html table. Default             
                            {
                                "bg-color": "white", 
                                "color": "black", 
                                "font-weight": "normal"
                            }
        tbl_style (optional): Table-specific styles, default 
                            {
                                "bg-color": "white", 
                                "color": "black", 
                                "font-weight": "normal"
                            }
        header_style (optional): Style for the table header, Default 
                                {
                                    "bg-color": "DarkViolet", 
                                    "color": "white", 
                                    "font-weight": "bold"
                                }
        cell_highlight (optional bool): Whether to highlight cells based on conditions.          Default is False.
        highlight_conditions (optional): A dictionary for conditional formatting. 
                                        For example, look below.
        content_based_color (optional bool): Whether to color cells based on content. Default is False.
        content_based_style (optional): Dictionary of styles based on content. The style will be applied for all column of same datatype 

        Supported keys are "String", "Int", "Float", "Boolean", "Datetime", "Date", "Time" and "Others". For example look below
        table_formatting (optional): Format of the table in the image. Possible values are:
            "ASCII_FULL"
            "ASCII_FULL_CONDENSED"
            "ASCII_NO_BORDERS"
            "ASCII_BORDERS_ONLY"
            "ASCII_BORDERS_ONLY_CONDENSED"
            "ASCII_HORIZONTAL_ONLY"
            "ASCII_MARKDOWN"
            "MARKDOWN"
            "NOTHING" Default is "ASCII_MARKDOWN".

        cell_padding (optional): Padding inside image cells. Default is 10.
        min_cell_width (optional): Minimum width for each image cell. Default is 100.
        float_precision (optional): Decimal precision for floating-point numbers. Default is 2.
        thousands_separator (optional): Character to use as a thousands separator. Default is _.
        return_type (optional): Type of output. Options are:

            "html" -> returns html string of the dataframe
            "pil_image" -> return PIL Image.
            Default is "pil_image".

image_to_bin:
    This function convert PIL Image to binary.

    Parameters:
        img (required): A PIL Image object.
        format (optional): The image format of the resultant binary(e.g., "PNG", "JPEG", etc.). Default is "PNG".
        
send_img_to_telegram:
    This is a addon function for sending PIL Image to Telegram chat via the Telegram Bot API.
    
    Parameters:
        img (required): A PIL Image object that you want to send to Telegram.
        chat_id (required): The chat ID of the recipient on Telegram.
        bot_token (required): Your Telegram bot token.
        img_name (optional): The name of the image file (without extension). Default is "sample".
        format (optional): The format of the image to send (e.g., "PNG", "JPEG"). Default is "PNG".

## Example ::

```python
import polars as pl
from datetime import datetime, date, time
from dfimg import df_to_html_img, send_img_to_telegram, image_to_bin

data = {
    "Title": ["x", "y", "z"],
    "Datetime": [datetime(2023, 1, 1), datetime(2023, 2, 1), datetime(2023, 3, 1)],
    "Date": [date(2023, 1, 1), date(2023, 2, 1), date(2023, 3, 1)],    
    "Time": [time(12, 0, 0), time(12, 0, 0), time(12, 0, 0)],
    "Int_col": [10, 20, 30],
    "Str_col": ["str1", "str2", "str3"],
    "Float_col": [1.5, 2.5, 3.5],
    "Bool_col": [True, False, True]
}

img = df_to_html_img(
        pl.DataFrame(data),
        title= "TEST",
        content_based_color= True,
        content_based_style= {
                        "String": {
                            "bg-color": "LightCoral", 
                            "color": "DodgerBlue", 
                            "font-weight": "bolder"
                            }
                        },
        cell_highlight= True,
        highlight_conditions= {
                        "Int_col": {
                                "condition": ">= 20", 
                                "bg-color": "yellow", 
                                "color": "green"
                                },
                        "Str_col": {
                                "condition": ".__contains__('str2')", 
                                "bg-color": "yellow", 
                                "color": "green"
                                },
                        "Bool_col": {
                                "condition": True, 
                                "bg-color": "yellow", 
                                "color": "green"
                                }
                            }
    )

# If your want to save the image locally:
img.save("image.png")

#for converting PIL Image to binary.

img_binary = image_to_bin(img)

#For sending image to telegram 

send_img_to_telegram(
                img= img, 
                chat_id= "xxxxxxxxx", 
                bot_token= "xxxxxxx:xxxxxxxxx"
                )


```

## Example Image ::
![Example](img/image.png)
