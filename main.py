import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# название 


# описание
st.title("Это тестовый сайт")
st.write("Загрузи CSV файла и заполни его")


## Шаг 1. Загрузка CSV файла
uploader_file = st.sidebar.file_uploader("Нажми сюда для загрузки файла", type="csv")
if uploader_file is not None:
    df = pd.read_csv(uploader_file)
    st.write(df.head())
else:
    st.stop()
    
## Шаг 2. Проверка наличия пропусков в файле
missed_value = df.isna().sum()

if (missed_value > 0).any():
    st.write(missed_value)
    fig, ax = plt.subplots()
    sns.barplot(x=missed_value.values.index, y=missed_value.values)
    ax.set_title("Пропущенные значения")
    st.pyplot(fig)

## Шаг 3. Заполнить пропуски
    button = st.sidebar.button('Заполнить пропуски')
    if button:
        df_filled = df[missed_values.index].copy()

        for col in df_filled.columns:
            if df_filled[col].dtype == 'object': #
                df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
            else: # Численные признаки
                df_filled[col] = df_filled[col].fillna(df_filled[col].median())

        st.write(df_filled.head(5))

## Шаг 4. Выгрузить заполнный от прпусков CSV файл
        download_button = st.sidebar.download_button(label='Скачать CSV файл', 
                   data=df_filled.to_csv(), 
                   file_name='filled_fate.csv')
else:
    st.write('Нет пропусков в данных.')
    # st.stop()
        
## Шаг 5. Добавление столбцов с датами.
if 'time_order' not in df.columns:
    datetime_df = pd.date_range(start='2023-01-01', end='2023-01-31', freq='D')
    df['time_order'] = np.random.choice(datetime_df, size=len(df))

## Шаг 6. Визуализация данных

if st.sidebar.button('График динамики чаевых по времени'):
    if 'time_order' in df.columns:
        df_sort_time = df.sort_values(by='time_order')
        fig1, ax1 = plt.subplots(figsize=(12, 7))
        sns.lineplot(x='time_order', y='total_bill', data=df_sort_time)
        plt.title('График динамики чаевых по времени.')
        plt.xlabel('Дата')
        plt.ylabel('Чаевые')
        st.pyplot(fig1)
    else:
        st.write("Столбец 'time_order' отсутствует в данных.")

if st.sidebar.button('Гистограмма количества оплат за заказ'):
    fig2 = plt.figure(figsize=(12, 7))
    sns.histplot(data=df, x=df['total_bill'])
    plt.xlabel('Оплата за заказ')
    plt.ylabel('Колчество оплат')
    plt.figtext(0.3, 0, 'Гистограмма количества оплат за заказ')
    st.pyplot(fig2)

if st.sidebar.button('График зависимости чаевых к сумме заказа'):
    fig3 = plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df, x='total_bill', y='tip', hue='total_bill')
    plt.xlabel('Оплата за заказ')
    plt.ylabel('Чаевые')
    plt.figtext(0.3, 0, 'График зависимости чаевых к сумме заказа')
    st.pyplot(fig3)

if st.sidebar.button('График зависимости чаевых к сумме заказа по размеру'):
    g = sns.relplot(data=df, x='total_bill', y='tip', hue='size', size='size', sizes=(10, 100), palette='pastel')
    g.set_axis_labels('Оплата за заказ', 'Чаевые')
    plt.figtext(0.1, 0, 'График зависимости чаевых к сумме заказа по размеру', fontsize=12)
    st.pyplot(g.fig)

# 
if 'day_of_week' not in df.columns:
    df['day_of_week'] = df['time_order'].dt.day_name()

if st.sidebar.button('Линейная связь между днем недели и размером счета'):
    fig5 = plt.figure(figsize=(12, 7))
    sns.lineplot(data=df, x='day_of_week', y='total_bill', color='green')
    plt.title('Связь между днем недели и размером счета')
    plt.xlabel('День недели')
    plt.ylabel('Размер счета')
    plt.xticks(rotation=45)
    st.pyplot(fig5)

if st.sidebar.button('Связь между днем недели и размером счета'):
    fig6 = plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df, x='tip', y='day_of_week', hue='sex', palette=['pink', 'blue'])
    plt.title('Связь между днем недели и чаевых по полу')
    plt.xlabel('Размер чаевых')
    plt.ylabel('День недели')
    st.pyplot(fig6)

if st.sidebar.button('Чаевые на обед и ланч'):
    fig7, ax2 = plt.subplots(1, 2, figsize=(14, 6))
    luntips = df[df['time'] == 'Lunch']['tip']
    dintips = df[df['time'] == 'Dinner']['tip']

    sns.histplot(luntips, bins=10, ax=ax2[0], color='orange', kde=True)
    ax2[0].set_title('Чаевые на обед')
    ax2[0].set_xlabel('Чаевые')
    ax2[0].set_ylabel('Количество')

    sns.histplot(dintips, bins=10, ax=ax2[1], color='blue', kde=True)
    ax2[1].set_title('Чаевые на ужин')
    ax2[1].set_xlabel('Чаевые')
    ax2[1].set_ylabel('Количество')

    plt.tight_layout()
    st.pyplot(fig7)

if st.sidebar.button('Размер счета и чаевые мужчин и женищин'):
    fig8, ax3 = plt.subplots(1, 2, figsize=(14, 6))
    sns.scatterplot(data=df[df['sex'] == 'Male'], 
                x='total_bill', 
                y='tip', 
                hue='smoker', 
                style='smoker',
                palette='deep',
                markers={'Yes': 'o', 'No': 'X'},
                ax=ax3[0])
    ax3[0].set_title('Мужчины: Размер счета vs. Чаевые')
    ax3[0].set_xlabel('Размер счета ($)')
    ax3[0].set_ylabel('Чаевые ($)')


    sns.scatterplot(data=df[df['sex'] == 'Female'], 
                    x='total_bill', 
                    y='tip', 
                    hue='smoker', 
                    style='smoker',
                    palette='deep',
                    markers={'Yes': 'o', 'No': 'X'},
                    ax=ax3[1])
    ax3[1].set_title('Женщины: Размер счета vs. Чаевые')
    ax3[1].set_xlabel('Размер счета ($)')
    ax3[1].set_ylabel('Чаевые ($)')
    plt.tight_layout()

    st.pyplot(fig8)
  