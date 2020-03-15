{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Using TensorFlow backend.\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import io\n",
    "import requests\n",
    "from datetime import datetime\n",
    "\n",
    "import statsmodels.api as sm\n",
    "import statsmodels.formula.api as sf\n",
    "\n",
    "import keras\n",
    "from keras.layers import Dense\n",
    "from keras.models import Sequential\n",
    "from keras.optimizers import Adam\n",
    "from keras.layers import LSTM\n",
    "\n",
    "\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from pylab import rcParams\n",
    "import chart_studio.plotly as py\n",
    "import plotly.graph_objects as go\n",
    "import plotly.offline as pyoff"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "#pip install tensorflow"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv(\"sample_data.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 6539 entries, 0 to 6538\n",
      "Columns: 106 entries, entity to appledistributor\n",
      "dtypes: float64(4), int64(91), object(11)\n",
      "memory usage: 5.3+ MB\n"
     ]
    }
   ],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>fromdate</th>\n",
       "      <th>titlecount</th>\n",
       "      <th>todate</th>\n",
       "      <th>amazontotalreviews</th>\n",
       "      <th>minappleprice</th>\n",
       "      <th>amazontotalrevenue</th>\n",
       "      <th>accruedpreordersoldunits</th>\n",
       "      <th>amazonlumpedpreordersubscriptionrevenue</th>\n",
       "      <th>preordersalesrevenue</th>\n",
       "      <th>foundatamazon</th>\n",
       "      <th>...</th>\n",
       "      <th>preorderrevenue</th>\n",
       "      <th>pubtrackreported</th>\n",
       "      <th>lumpedpreorderrevenue</th>\n",
       "      <th>amazonsoldunits</th>\n",
       "      <th>amazonpreordersubscriptionrevenue</th>\n",
       "      <th>preordersubscriptionunits</th>\n",
       "      <th>amazonpreordersalesrevenue</th>\n",
       "      <th>maxappleprice</th>\n",
       "      <th>pagelength</th>\n",
       "      <th>pricewassetbypublisher</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>count</td>\n",
       "      <td>6.539000e+03</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6.539000e+03</td>\n",
       "      <td>6522.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.0</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>...</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.0</td>\n",
       "      <td>6539.0</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>6539.000000</td>\n",
       "      <td>2558.000000</td>\n",
       "      <td>1531.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>mean</td>\n",
       "      <td>2.018078e+07</td>\n",
       "      <td>1.599174</td>\n",
       "      <td>2.018080e+07</td>\n",
       "      <td>242.896044</td>\n",
       "      <td>118.859459</td>\n",
       "      <td>18074.906866</td>\n",
       "      <td>0.235204</td>\n",
       "      <td>0.0</td>\n",
       "      <td>155.503288</td>\n",
       "      <td>0.998165</td>\n",
       "      <td>...</td>\n",
       "      <td>155.503288</td>\n",
       "      <td>0.984095</td>\n",
       "      <td>155.503288</td>\n",
       "      <td>17.666004</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>155.503288</td>\n",
       "      <td>118.859459</td>\n",
       "      <td>336.532447</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>std</td>\n",
       "      <td>7.319859e+03</td>\n",
       "      <td>0.748654</td>\n",
       "      <td>7.321285e+03</td>\n",
       "      <td>57.042772</td>\n",
       "      <td>323.464108</td>\n",
       "      <td>30999.078107</td>\n",
       "      <td>2.776806</td>\n",
       "      <td>0.0</td>\n",
       "      <td>8769.366153</td>\n",
       "      <td>0.042803</td>\n",
       "      <td>...</td>\n",
       "      <td>8769.366153</td>\n",
       "      <td>0.125116</td>\n",
       "      <td>8769.366153</td>\n",
       "      <td>36.272170</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>8769.366153</td>\n",
       "      <td>323.464108</td>\n",
       "      <td>42.531144</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>min</td>\n",
       "      <td>2.017040e+07</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>2.017040e+07</td>\n",
       "      <td>120.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>...</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>305.000000</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>25%</td>\n",
       "      <td>2.017121e+07</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>2.017121e+07</td>\n",
       "      <td>200.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1998.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>...</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>320.000000</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>50%</td>\n",
       "      <td>2.018071e+07</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>2.018071e+07</td>\n",
       "      <td>250.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>7191.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>...</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>6.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>321.000000</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>75%</td>\n",
       "      <td>2.019013e+07</td>\n",
       "      <td>2.000000</td>\n",
       "      <td>2.019013e+07</td>\n",
       "      <td>283.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>17982.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>...</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>13.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>321.000000</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>max</td>\n",
       "      <td>2.019083e+07</td>\n",
       "      <td>4.000000</td>\n",
       "      <td>2.019083e+07</td>\n",
       "      <td>331.000000</td>\n",
       "      <td>999.000000</td>\n",
       "      <td>571692.000000</td>\n",
       "      <td>82.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>501420.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>...</td>\n",
       "      <td>501420.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>501420.000000</td>\n",
       "      <td>781.000000</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>501420.000000</td>\n",
       "      <td>999.000000</td>\n",
       "      <td>496.000000</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>8 rows × 95 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "           fromdate   titlecount        todate  amazontotalreviews  \\\n",
       "count  6.539000e+03  6539.000000  6.539000e+03         6522.000000   \n",
       "mean   2.018078e+07     1.599174  2.018080e+07          242.896044   \n",
       "std    7.319859e+03     0.748654  7.321285e+03           57.042772   \n",
       "min    2.017040e+07     1.000000  2.017040e+07          120.000000   \n",
       "25%    2.017121e+07     1.000000  2.017121e+07          200.000000   \n",
       "50%    2.018071e+07     1.000000  2.018071e+07          250.000000   \n",
       "75%    2.019013e+07     2.000000  2.019013e+07          283.000000   \n",
       "max    2.019083e+07     4.000000  2.019083e+07          331.000000   \n",
       "\n",
       "       minappleprice  amazontotalrevenue  accruedpreordersoldunits  \\\n",
       "count    6539.000000         6539.000000               6539.000000   \n",
       "mean      118.859459        18074.906866                  0.235204   \n",
       "std       323.464108        30999.078107                  2.776806   \n",
       "min         0.000000            0.000000                  0.000000   \n",
       "25%         0.000000         1998.000000                  0.000000   \n",
       "50%         0.000000         7191.000000                  0.000000   \n",
       "75%         0.000000        17982.000000                  0.000000   \n",
       "max       999.000000       571692.000000                 82.000000   \n",
       "\n",
       "       amazonlumpedpreordersubscriptionrevenue  preordersalesrevenue  \\\n",
       "count                                   6539.0           6539.000000   \n",
       "mean                                       0.0            155.503288   \n",
       "std                                        0.0           8769.366153   \n",
       "min                                        0.0              0.000000   \n",
       "25%                                        0.0              0.000000   \n",
       "50%                                        0.0              0.000000   \n",
       "75%                                        0.0              0.000000   \n",
       "max                                        0.0         501420.000000   \n",
       "\n",
       "       foundatamazon  ...  preorderrevenue  pubtrackreported  \\\n",
       "count    6539.000000  ...      6539.000000       6539.000000   \n",
       "mean        0.998165  ...       155.503288          0.984095   \n",
       "std         0.042803  ...      8769.366153          0.125116   \n",
       "min         0.000000  ...         0.000000          0.000000   \n",
       "25%         1.000000  ...         0.000000          1.000000   \n",
       "50%         1.000000  ...         0.000000          1.000000   \n",
       "75%         1.000000  ...         0.000000          1.000000   \n",
       "max         1.000000  ...    501420.000000          1.000000   \n",
       "\n",
       "       lumpedpreorderrevenue  amazonsoldunits  \\\n",
       "count            6539.000000      6539.000000   \n",
       "mean              155.503288        17.666004   \n",
       "std              8769.366153        36.272170   \n",
       "min                 0.000000         0.000000   \n",
       "25%                 0.000000         1.000000   \n",
       "50%                 0.000000         6.000000   \n",
       "75%                 0.000000        13.000000   \n",
       "max            501420.000000       781.000000   \n",
       "\n",
       "       amazonpreordersubscriptionrevenue  preordersubscriptionunits  \\\n",
       "count                             6539.0                     6539.0   \n",
       "mean                                 0.0                        0.0   \n",
       "std                                  0.0                        0.0   \n",
       "min                                  0.0                        0.0   \n",
       "25%                                  0.0                        0.0   \n",
       "50%                                  0.0                        0.0   \n",
       "75%                                  0.0                        0.0   \n",
       "max                                  0.0                        0.0   \n",
       "\n",
       "       amazonpreordersalesrevenue  maxappleprice   pagelength  \\\n",
       "count                 6539.000000    6539.000000  2558.000000   \n",
       "mean                   155.503288     118.859459   336.532447   \n",
       "std                   8769.366153     323.464108    42.531144   \n",
       "min                      0.000000       0.000000   305.000000   \n",
       "25%                      0.000000       0.000000   320.000000   \n",
       "50%                      0.000000       0.000000   321.000000   \n",
       "75%                      0.000000       0.000000   321.000000   \n",
       "max                 501420.000000     999.000000   496.000000   \n",
       "\n",
       "       pricewassetbypublisher  \n",
       "count                  1531.0  \n",
       "mean                      1.0  \n",
       "std                       0.0  \n",
       "min                       1.0  \n",
       "25%                       1.0  \n",
       "50%                       1.0  \n",
       "75%                       1.0  \n",
       "max                       1.0  \n",
       "\n",
       "[8 rows x 95 columns]"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>entity</th>\n",
       "      <th>formattype</th>\n",
       "      <th>fromdate</th>\n",
       "      <th>titlecount</th>\n",
       "      <th>titles</th>\n",
       "      <th>todate</th>\n",
       "      <th>author</th>\n",
       "      <th>amazontotalreviews</th>\n",
       "      <th>minappleprice</th>\n",
       "      <th>amazontotalrevenue</th>\n",
       "      <th>...</th>\n",
       "      <th>lumpedpreorderrevenue</th>\n",
       "      <th>amazonsoldunits</th>\n",
       "      <th>amazonpreordersubscriptionrevenue</th>\n",
       "      <th>preordersubscriptionunits</th>\n",
       "      <th>amazonpreordersalesrevenue</th>\n",
       "      <th>maxappleprice</th>\n",
       "      <th>pagelength</th>\n",
       "      <th>pricewassetbypublisher</th>\n",
       "      <th>barnesandnobledistributor</th>\n",
       "      <th>appledistributor</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>20170418</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>20170419</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>20170419</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>20170420</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>702</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>20170420</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>20170421</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>4914</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>20170421</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>20170422</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>4212</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>20170422</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>20170423</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>702</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>5 rows × 106 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "              entity formattype  fromdate  titlecount  \\\n",
       "0  Alone in the dark      print  20170418           1   \n",
       "1  Alone in the dark      print  20170419           1   \n",
       "2  Alone in the dark      print  20170420           1   \n",
       "3  Alone in the dark      print  20170421           1   \n",
       "4  Alone in the dark      print  20170422           1   \n",
       "\n",
       "                                              titles    todate         author  \\\n",
       "0  {'amazontotalreviews': 306, 'minappleprice': 0...  20170419  Frith Banbury   \n",
       "1  {'amazontotalreviews': 306, 'minappleprice': 0...  20170420  Frith Banbury   \n",
       "2  {'amazontotalreviews': 306, 'minappleprice': 0...  20170421  Frith Banbury   \n",
       "3  {'amazontotalreviews': 306, 'minappleprice': 0...  20170422  Frith Banbury   \n",
       "4  {'amazontotalreviews': 306, 'minappleprice': 0...  20170423  Frith Banbury   \n",
       "\n",
       "   amazontotalreviews  minappleprice  amazontotalrevenue  ...  \\\n",
       "0               306.0              0                   0  ...   \n",
       "1               306.0              0                 702  ...   \n",
       "2               306.0              0                4914  ...   \n",
       "3               306.0              0                4212  ...   \n",
       "4               306.0              0                 702  ...   \n",
       "\n",
       "   lumpedpreorderrevenue  amazonsoldunits  amazonpreordersubscriptionrevenue  \\\n",
       "0                      0                6                                  0   \n",
       "1                      0                7                                  0   \n",
       "2                      0                7                                  0   \n",
       "3                      0                6                                  0   \n",
       "4                      0                1                                  0   \n",
       "\n",
       "   preordersubscriptionunits  amazonpreordersalesrevenue  maxappleprice  \\\n",
       "0                          0                           0              0   \n",
       "1                          0                           0              0   \n",
       "2                          0                           0              0   \n",
       "3                          0                           0              0   \n",
       "4                          0                           0              0   \n",
       "\n",
       "   pagelength  pricewassetbypublisher  barnesandnobledistributor  \\\n",
       "0         NaN                     NaN                        NaN   \n",
       "1         NaN                     NaN                        NaN   \n",
       "2         NaN                     NaN                        NaN   \n",
       "3         NaN                     NaN                        NaN   \n",
       "4         NaN                     NaN                        NaN   \n",
       "\n",
       "   appledistributor  \n",
       "0               NaN  \n",
       "1               NaN  \n",
       "2               NaN  \n",
       "3               NaN  \n",
       "4               NaN  \n",
       "\n",
       "[5 rows x 106 columns]"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Cleaning"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "entity                          0\n",
      "formattype                      0\n",
      "fromdate                        0\n",
      "titlecount                      0\n",
      "titles                          0\n",
      "                             ... \n",
      "maxappleprice                   0\n",
      "pagelength                   3981\n",
      "pricewassetbypublisher       5008\n",
      "barnesandnobledistributor    4804\n",
      "appledistributor             5783\n",
      "Length: 106, dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(df.isnull().sum())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "entity                        object\n",
       "formattype                    object\n",
       "fromdate                       int64\n",
       "titlecount                     int64\n",
       "titles                        object\n",
       "                              ...   \n",
       "maxappleprice                  int64\n",
       "pagelength                   float64\n",
       "pricewassetbypublisher       float64\n",
       "barnesandnobledistributor     object\n",
       "appledistributor              object\n",
       "Length: 106, dtype: object"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.dtypes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "df['fromdate']=pd.to_datetime(df['fromdate'], format =\"%Y%m%d\")\n",
    "df['todate']=pd.to_datetime(df['todate'], format =\"%Y%m%d\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>entity</th>\n",
       "      <th>formattype</th>\n",
       "      <th>fromdate</th>\n",
       "      <th>titlecount</th>\n",
       "      <th>titles</th>\n",
       "      <th>todate</th>\n",
       "      <th>author</th>\n",
       "      <th>amazontotalreviews</th>\n",
       "      <th>minappleprice</th>\n",
       "      <th>amazontotalrevenue</th>\n",
       "      <th>...</th>\n",
       "      <th>lumpedpreorderrevenue</th>\n",
       "      <th>amazonsoldunits</th>\n",
       "      <th>amazonpreordersubscriptionrevenue</th>\n",
       "      <th>preordersubscriptionunits</th>\n",
       "      <th>amazonpreordersalesrevenue</th>\n",
       "      <th>maxappleprice</th>\n",
       "      <th>pagelength</th>\n",
       "      <th>pricewassetbypublisher</th>\n",
       "      <th>barnesandnobledistributor</th>\n",
       "      <th>appledistributor</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-18</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>2017-04-19</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-19</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>2017-04-20</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>702</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-20</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>2017-04-21</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>4914</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-21</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>2017-04-22</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>4212</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-22</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>2017-04-23</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306.0</td>\n",
       "      <td>0</td>\n",
       "      <td>702</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6534</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-22</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>2019-08-23</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275.0</td>\n",
       "      <td>0</td>\n",
       "      <td>81835</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>25</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6535</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-23</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>2019-08-24</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275.0</td>\n",
       "      <td>0</td>\n",
       "      <td>18460</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6536</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-24</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>2019-08-25</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275.0</td>\n",
       "      <td>0</td>\n",
       "      <td>38623</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>12</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6537</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-25</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275.0</td>\n",
       "      <td>0</td>\n",
       "      <td>80340</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>25</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6538</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>2019-08-27</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275.0</td>\n",
       "      <td>0</td>\n",
       "      <td>43212</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>13</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>6539 rows × 106 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                 entity formattype   fromdate  titlecount  \\\n",
       "0     Alone in the dark      print 2017-04-18           1   \n",
       "1     Alone in the dark      print 2017-04-19           1   \n",
       "2     Alone in the dark      print 2017-04-20           1   \n",
       "3     Alone in the dark      print 2017-04-21           1   \n",
       "4     Alone in the dark      print 2017-04-22           1   \n",
       "...                 ...        ...        ...         ...   \n",
       "6534   The Walking Dead      audio 2019-08-22           1   \n",
       "6535   The Walking Dead      audio 2019-08-23           1   \n",
       "6536   The Walking Dead      audio 2019-08-24           1   \n",
       "6537   The Walking Dead      audio 2019-08-25           1   \n",
       "6538   The Walking Dead      audio 2019-08-26           1   \n",
       "\n",
       "                                                 titles     todate  \\\n",
       "0     {'amazontotalreviews': 306, 'minappleprice': 0... 2017-04-19   \n",
       "1     {'amazontotalreviews': 306, 'minappleprice': 0... 2017-04-20   \n",
       "2     {'amazontotalreviews': 306, 'minappleprice': 0... 2017-04-21   \n",
       "3     {'amazontotalreviews': 306, 'minappleprice': 0... 2017-04-22   \n",
       "4     {'amazontotalreviews': 306, 'minappleprice': 0... 2017-04-23   \n",
       "...                                                 ...        ...   \n",
       "6534  {'amazontotalreviews': 275, 'minappleprice': 0... 2019-08-23   \n",
       "6535  {'amazontotalreviews': 275, 'minappleprice': 0... 2019-08-24   \n",
       "6536  {'amazontotalreviews': 275, 'minappleprice': 0... 2019-08-25   \n",
       "6537  {'amazontotalreviews': 275, 'minappleprice': 0... 2019-08-26   \n",
       "6538  {'amazontotalreviews': 275, 'minappleprice': 0... 2019-08-27   \n",
       "\n",
       "               author  amazontotalreviews  minappleprice  amazontotalrevenue  \\\n",
       "0       Frith Banbury               306.0              0                   0   \n",
       "1       Frith Banbury               306.0              0                 702   \n",
       "2       Frith Banbury               306.0              0                4914   \n",
       "3       Frith Banbury               306.0              0                4212   \n",
       "4       Frith Banbury               306.0              0                 702   \n",
       "...               ...                 ...            ...                 ...   \n",
       "6534  Matthew Murdock               275.0              0               81835   \n",
       "6535  Matthew Murdock               275.0              0               18460   \n",
       "6536  Matthew Murdock               275.0              0               38623   \n",
       "6537  Matthew Murdock               275.0              0               80340   \n",
       "6538  Matthew Murdock               275.0              0               43212   \n",
       "\n",
       "      ...  lumpedpreorderrevenue  amazonsoldunits  \\\n",
       "0     ...                      0                6   \n",
       "1     ...                      0                7   \n",
       "2     ...                      0                7   \n",
       "3     ...                      0                6   \n",
       "4     ...                      0                1   \n",
       "...   ...                    ...              ...   \n",
       "6534  ...                      0               25   \n",
       "6535  ...                      0                5   \n",
       "6536  ...                      0               12   \n",
       "6537  ...                      0               25   \n",
       "6538  ...                      0               13   \n",
       "\n",
       "      amazonpreordersubscriptionrevenue  preordersubscriptionunits  \\\n",
       "0                                     0                          0   \n",
       "1                                     0                          0   \n",
       "2                                     0                          0   \n",
       "3                                     0                          0   \n",
       "4                                     0                          0   \n",
       "...                                 ...                        ...   \n",
       "6534                                  0                          0   \n",
       "6535                                  0                          0   \n",
       "6536                                  0                          0   \n",
       "6537                                  0                          0   \n",
       "6538                                  0                          0   \n",
       "\n",
       "      amazonpreordersalesrevenue  maxappleprice  pagelength  \\\n",
       "0                              0              0         NaN   \n",
       "1                              0              0         NaN   \n",
       "2                              0              0         NaN   \n",
       "3                              0              0         NaN   \n",
       "4                              0              0         NaN   \n",
       "...                          ...            ...         ...   \n",
       "6534                           0              0       395.0   \n",
       "6535                           0              0       395.0   \n",
       "6536                           0              0       395.0   \n",
       "6537                           0              0       395.0   \n",
       "6538                           0              0       395.0   \n",
       "\n",
       "      pricewassetbypublisher  barnesandnobledistributor  appledistributor  \n",
       "0                        NaN                        NaN               NaN  \n",
       "1                        NaN                        NaN               NaN  \n",
       "2                        NaN                        NaN               NaN  \n",
       "3                        NaN                        NaN               NaN  \n",
       "4                        NaN                        NaN               NaN  \n",
       "...                      ...                        ...               ...  \n",
       "6534                     NaN                        NaN               NaN  \n",
       "6535                     NaN                        NaN               NaN  \n",
       "6536                     NaN                        NaN               NaN  \n",
       "6537                     NaN                        NaN               NaN  \n",
       "6538                     NaN                        NaN               NaN  \n",
       "\n",
       "[6539 rows x 106 columns]"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.fillna(0, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "df['amazontotalreviews'] = df['amazontotalreviews'].astype(int)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration/ Data Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "#group entitys by year and month:\n",
    "df2 = df['entity'].groupby([df['entity'], df['formats'], df['formattype']]).agg(('count'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "entity             formats                               formattype\n",
       "Alone in the dark  Audible                               audio          19\n",
       "                   Audible Audiobook                     audio         299\n",
       "                   Audible Book                          audio          12\n",
       "                   Audio CD                              print         789\n",
       "                   Audiobook                             audio         291\n",
       "                   Hardcover                             print         248\n",
       "                   Kindle Edition                        ebook          19\n",
       "                   Kindle Edition,NOOK Book              ebook         863\n",
       "                   Mass Market Paperback                 print         477\n",
       "                   NOOK Book                             ebook           5\n",
       "                   Paperback                             print          18\n",
       "The Walking Dead   0                                     audio           1\n",
       "                   Audible                               audio          27\n",
       "                   Audible Audio Edition                 audio           1\n",
       "                   Audible Audiobook                     audio         418\n",
       "                   Audible Book                          audio          17\n",
       "                   Audio CD                              print          92\n",
       "                   Audiobook                             audio         383\n",
       "                   Hardcover                             print         861\n",
       "                   Kindle Edition                        ebook           3\n",
       "                   Kindle Edition,Apple iBook            ebook           4\n",
       "                   Kindle Edition,Apple iBook,NOOK Book  ebook         752\n",
       "                   Kindle Edition,NOOK Book              ebook         104\n",
       "                   NOOK Book                             ebook          11\n",
       "                   Paperback                             print         825\n",
       "Name: entity, dtype: int64"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['Alone in the dark', 'The Walking Dead'], dtype=object)"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['entity'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['Frith Banbury', 'Matthew Murdock'], dtype=object)"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['author'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['bigfive', 'uncategorizedmanyauthor'], dtype=object)"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['publishertype'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['Simon & Schuster', 'Pocket',\n",
       "       'Simon & Schuster Audio and Blackstone Audio'], dtype=object)"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['publisherparent'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['print', 'ebook', 'audio'], dtype=object)"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['formattype'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_grouped=df.groupby(['entity','fromdate','todate','formattype', 'formats']).agg(totalrevenue=pd.NamedAgg(column='totalrevenue', aggfunc=sum),\n",
    "                                                                                     totalreviews=pd.NamedAgg(column='amazontotalreviews', aggfunc=sum)) \n",
    "                                                                                    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_grouped.reset_index(inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>entity</th>\n",
       "      <th>fromdate</th>\n",
       "      <th>todate</th>\n",
       "      <th>formattype</th>\n",
       "      <th>formats</th>\n",
       "      <th>totalrevenue</th>\n",
       "      <th>totalreviews</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>2017-04-04</td>\n",
       "      <td>2017-04-05</td>\n",
       "      <td>ebook</td>\n",
       "      <td>Kindle Edition</td>\n",
       "      <td>10485</td>\n",
       "      <td>306</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>2017-04-05</td>\n",
       "      <td>2017-04-06</td>\n",
       "      <td>ebook</td>\n",
       "      <td>Kindle Edition</td>\n",
       "      <td>8388</td>\n",
       "      <td>306</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>2017-04-06</td>\n",
       "      <td>2017-04-07</td>\n",
       "      <td>ebook</td>\n",
       "      <td>Kindle Edition</td>\n",
       "      <td>6990</td>\n",
       "      <td>306</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>2017-04-07</td>\n",
       "      <td>2017-04-08</td>\n",
       "      <td>audio</td>\n",
       "      <td>Audible</td>\n",
       "      <td>2990</td>\n",
       "      <td>306</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>2017-04-07</td>\n",
       "      <td>2017-04-08</td>\n",
       "      <td>ebook</td>\n",
       "      <td>Kindle Edition</td>\n",
       "      <td>4194</td>\n",
       "      <td>306</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6534</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>2019-08-25</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>print</td>\n",
       "      <td>Paperback</td>\n",
       "      <td>84185</td>\n",
       "      <td>275</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6535</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>2019-08-27</td>\n",
       "      <td>audio</td>\n",
       "      <td>Audible Audiobook</td>\n",
       "      <td>43212</td>\n",
       "      <td>275</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6536</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>2019-08-27</td>\n",
       "      <td>ebook</td>\n",
       "      <td>Kindle Edition,Apple iBook,NOOK Book</td>\n",
       "      <td>11988</td>\n",
       "      <td>275</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6537</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>2019-08-27</td>\n",
       "      <td>print</td>\n",
       "      <td>Hardcover</td>\n",
       "      <td>5888</td>\n",
       "      <td>275</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6538</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>2019-08-27</td>\n",
       "      <td>print</td>\n",
       "      <td>Paperback</td>\n",
       "      <td>45445</td>\n",
       "      <td>275</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>6539 rows × 7 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                 entity   fromdate     todate formattype  \\\n",
       "0     Alone in the dark 2017-04-04 2017-04-05      ebook   \n",
       "1     Alone in the dark 2017-04-05 2017-04-06      ebook   \n",
       "2     Alone in the dark 2017-04-06 2017-04-07      ebook   \n",
       "3     Alone in the dark 2017-04-07 2017-04-08      audio   \n",
       "4     Alone in the dark 2017-04-07 2017-04-08      ebook   \n",
       "...                 ...        ...        ...        ...   \n",
       "6534   The Walking Dead 2019-08-25 2019-08-26      print   \n",
       "6535   The Walking Dead 2019-08-26 2019-08-27      audio   \n",
       "6536   The Walking Dead 2019-08-26 2019-08-27      ebook   \n",
       "6537   The Walking Dead 2019-08-26 2019-08-27      print   \n",
       "6538   The Walking Dead 2019-08-26 2019-08-27      print   \n",
       "\n",
       "                                   formats  totalrevenue  totalreviews  \n",
       "0                           Kindle Edition         10485           306  \n",
       "1                           Kindle Edition          8388           306  \n",
       "2                           Kindle Edition          6990           306  \n",
       "3                                  Audible          2990           306  \n",
       "4                           Kindle Edition          4194           306  \n",
       "...                                    ...           ...           ...  \n",
       "6534                             Paperback         84185           275  \n",
       "6535                     Audible Audiobook         43212           275  \n",
       "6536  Kindle Edition,Apple iBook,NOOK Book         11988           275  \n",
       "6537                             Hardcover          5888           275  \n",
       "6538                             Paperback         45445           275  \n",
       "\n",
       "[6539 rows x 7 columns]"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_grouped"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1509.77x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "g = sns.catplot(\"formats\", \"totalrevenue\", data =df_grouped, hue=\"entity\",\n",
    "                  kind=\"bar\",palette=\"husl\",height=8,aspect=2.4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1855.38x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "g = sns.catplot(\"formats\", \"totalreviews\", data =df_grouped, hue=\"entity\",\n",
    "                  kind=\"bar\",palette=\"husl\",height=8,aspect=3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Count each Entity based on month and year:\n",
    "entity_count= df['entity'].groupby([df['entity'],df['formattype'],df['formats'],df['todate'].dt.year.rename('Year'), df['todate'].dt.month.rename('Month')]).agg({'count'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "entity_count.reset_index(inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>entity</th>\n",
       "      <th>formattype</th>\n",
       "      <th>formats</th>\n",
       "      <th>Year</th>\n",
       "      <th>Month</th>\n",
       "      <th>count</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>audio</td>\n",
       "      <td>Audible</td>\n",
       "      <td>2017</td>\n",
       "      <td>4</td>\n",
       "      <td>4</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>audio</td>\n",
       "      <td>Audible</td>\n",
       "      <td>2017</td>\n",
       "      <td>5</td>\n",
       "      <td>11</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>audio</td>\n",
       "      <td>Audible</td>\n",
       "      <td>2017</td>\n",
       "      <td>6</td>\n",
       "      <td>4</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>audio</td>\n",
       "      <td>Audible Audiobook</td>\n",
       "      <td>2017</td>\n",
       "      <td>5</td>\n",
       "      <td>3</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>audio</td>\n",
       "      <td>Audible Audiobook</td>\n",
       "      <td>2017</td>\n",
       "      <td>6</td>\n",
       "      <td>2</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>278</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>print</td>\n",
       "      <td>Paperback</td>\n",
       "      <td>2019</td>\n",
       "      <td>4</td>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>279</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>print</td>\n",
       "      <td>Paperback</td>\n",
       "      <td>2019</td>\n",
       "      <td>5</td>\n",
       "      <td>31</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>280</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>print</td>\n",
       "      <td>Paperback</td>\n",
       "      <td>2019</td>\n",
       "      <td>6</td>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>281</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>print</td>\n",
       "      <td>Paperback</td>\n",
       "      <td>2019</td>\n",
       "      <td>7</td>\n",
       "      <td>31</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>282</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>print</td>\n",
       "      <td>Paperback</td>\n",
       "      <td>2019</td>\n",
       "      <td>8</td>\n",
       "      <td>27</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>283 rows × 6 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                entity formattype            formats  Year  Month  count\n",
       "0    Alone in the dark      audio            Audible  2017      4      4\n",
       "1    Alone in the dark      audio            Audible  2017      5     11\n",
       "2    Alone in the dark      audio            Audible  2017      6      4\n",
       "3    Alone in the dark      audio  Audible Audiobook  2017      5      3\n",
       "4    Alone in the dark      audio  Audible Audiobook  2017      6      2\n",
       "..                 ...        ...                ...   ...    ...    ...\n",
       "278   The Walking Dead      print          Paperback  2019      4     30\n",
       "279   The Walking Dead      print          Paperback  2019      5     31\n",
       "280   The Walking Dead      print          Paperback  2019      6     30\n",
       "281   The Walking Dead      print          Paperback  2019      7     31\n",
       "282   The Walking Dead      print          Paperback  2019      8     27\n",
       "\n",
       "[283 rows x 6 columns]"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "entity_count"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAABeUAAAFgCAYAAAA1lBKLAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAgAElEQVR4nOzde5jXZZ0//ufAcHBBRMgRD7gtmmlomCck0hIKDzgyiHioVFBj+16rg+hiBEqtpe7a5kKl2WyujbuaqwgzGagIulKetpCyzCzRVWCVUQ4qoOMwzO8Pf85GjgMo82agx+O6uK7P3O/7/bpfH6754zPPued+lzQ1NTUFAAAAAABocx22dQMAAAAAAPCXQigPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABSkXYfy55133rZuAQAAAAAAtpp2HcqvWrVqW7cAAAAAAABbTbsO5QEAAAAAYEcilAcAAAAAgIII5QEAAAAAoCBCeQAAAAAAKIhQHgAAAAAACiKUBwAAAACAggjlAQAAAACgIEJ5AAAAAAAoiFAeAAAAAAAKIpQHAAAAAICCCOUBAAAAAKAgQnkAAAAAACiIUB4AAAAAAAoilAfapab19du6BWhzvs8BAADgL0/ptm4AoCUlpV3ywhUHb+s2oE3tM/U327oFAAAAoGB2ygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBB2iSUf+2111JZWZnjjz8+J5xwQhYtWpTVq1dn7NixGTZsWMaOHZtXX321LZYGAAAAAIB2q01C+SuvvDJHH3107rnnntTW1mbfffdNVVVVBg0alLlz52bQoEGpqqpqi6UBAAAAAKDd2uqh/Jo1a/KLX/wip556apKkc+fO6dGjR+bPn5+KiookSUVFRebNm7e1lwYAAAAAgHatdGsXXLJkSXr16pWvfvWr+f3vf5/+/ftnypQpWbFiRcrKypIkZWVlWbly5dZeGgAAAAAA2rWtvlN+/fr1+d3vfpczzzwzNTU12WmnnRxVAwAAAAAAaYNQvk+fPunTp08GDBiQJDn++OPzu9/9Lr17905dXV2SpK6uLr169draSwMAAAAAQLu21UP53XbbLX369Mmzzz6bJHnkkUey7777ZsiQIampqUmS1NTUZOjQoVt7aQAAAAAAaNe2+pnySXL55Zfn7//+79PQ0JC+ffvm6quvzoYNG3LRRRdlxowZ2WOPPTJ9+vS2WBoAAAAAANqtNgnlDzzwwMycOfNd49XV1W2xHAAAAAAAbBe2+vE1AAAAAABAy4TyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAQEGa1tdv6xagzfk+B2hd6bZuAAAAAP5SlJR2yQtXHLyt24A2tc/U32zrFgDatTYL5YcMGZJu3bqlQ4cO6dixY2bOnJnVq1dnwoQJWbZsWfbaa69MmzYtu+yyS1u1AAAAAAAA7UqbHl9TXV2d2trazJw5M0lSVVWVQYMGZe7cuRk0aFCqqqracnkAAAAAAGhXCj1Tfv78+amoqEiSVFRUZN68eUUuDwAAAAAA21SbhvLnnXdeTjnllPznf/5nkmTFihUpKytLkpSVlWXlypVtuTwAALAdqW9o3NYtAABAm2uzM+V//OMfZ/fdd8+KFSsyduzY9OvXr62WAgAAdgBdOnXMYRNv3tZtQJta+K2zt3ULAMA21mY75XffffckSe/evfO5z30uTzzxRHr37p26urokSV1dXXr16tVWywMAAAAAQLvTJqH8unXrsmbNmubXDz30UD7ykY9kyJAhqampSZLU1NRk6NChbbE8AAAAAAC0S21yfM2KFSvyd3/3d0mSxsbGnHTSSTnmmGNy8MEH56KLLsqMGTOyxx57ZPr06W2xPAAAAAAAtEttEsr37ds3P/nJT941vuuuu6a6urotlgQAAAAAgHavzc6UBwAAAAAANiaUBwAAAACAggjlAQAAAACgIEJ5AAAAAAAoiFAeAAAAAAAKIpQHAAAAAICCCOUBAAAAAKAgQnkAAAAAACiIUB4AAAAAAAoilAcAAAAAgIII5QEAAAAAoCBCeQAAAAAAKIhQHgAAAAAACiKUBwAAAACAggjlAQAAAACgIEJ5AAAAAAAoiFAeAAAAAAAKIpTfDtU3NG7rFgAAAAAAeB9Kt3UDbLkunTrmsIk3b+s2oE0t/NbZ27oFAAAAANjq7JQHAAAAAICCCOUBAAAAAKAgQnkAAAAAACiIUB4AAAAAAAoilAcAAAAAgIII5QEAAAAAoCBCeQAAAAAAKIhQHgAAAAAACiKUBwAAAACAggjlAQAAAACgIEJ5AAAAAAAoiFAeAAAAAAAKIpQHAAAAAICCCOUBAAAAAKAgrYby69aty4YNG5Ikzz33XObPn5+GhoZCGgMAAAAAgB1Nq6H8F7/4xdTX12f58uUZM2ZMZs6cmUmTJhXVGwAAAAAA7FBaDeWbmpqy0047Ze7cufniF7+Y6667LosXLy6qNwAAAAAA2KFsMpRftGhR7rrrrnzmM59JkjQ2NhbRFwAAAAAA7HBaDeUnT56cH/zgB/nsZz+bj3zkI1myZEkGDhxYVG8AAAAAALBDKW3t4pFHHpkjjzwy69atS5L07ds3l1122WYVbmxszKhRo7L77rvnBz/4QZYsWZKLL744r776aj72sY/lmmuuSefOnT/4OwAAAAAAgO1EqzvlFy1alBNPPDEnnnhikuT3v/99vv71r29W4Ztvvjn77rtv89f//M//nDFjxmTu3Lnp0aNHZsyY8f67BgAAAACA7VCrofxVV12VG2+8MT179kySHHDAAfnlL3+5yaIvvfRS/uu//iunnnpqkrfPpn/00Udz3HHHJUlGjhyZ+fPnf9DeAQAAAABgu9JqKJ8ke+yxx8Y3dNjkLbnqqqsyceLE5rmrVq1Kjx49Ulr69mk5ffr0yfLly99PvwAAAAAAsN1qNWHfY4898vjjj6ekpCRvvfVWbrzxxo2OpGnJAw88kF69euWggw5qdV5JScmWdwsAAAAAANuxVh/0+vWvfz1XXnllli9fnk9/+tMZPHhwpk6d2mrBxx9/PPfff38WLFiQ+vr6rFmzJldeeWVee+21rF+/PqWlpXnppZdSVla2Vd8IAAAAAAC0d62G8r169cq3v/3tLSp4ySWX5JJLLkmSPPbYY/m3f/u3fPvb305lZWXuvffeDB8+PLNmzcqQIUPef9cAAAAAALAdajGU/9d//dd86Utfyje+8Y0Wj5m57LLLtnihiRMnZsKECZk2bVoOPPDAjB49esu7BQAAAACA7ViLofw758Zv6lz4TRk4cGAGDhyYJOnbt29mzJjxgeoBAAAAAMD2rMVQ/p2jZbp27ZoTTjhho2t3331323cFAAAAAAA7oA6tXayqqtqsMQAAAAAAYNNa3Cn/4IMPZsGCBVm+fHm++c1vNo+vWbMmHTt2LKw5AAAAAADYkbQYyu++++456KCDcv/996d///7N4926dctXv/rVwpoDgB1Z/fr6dCntsq3bgDbl+xwAAGBjLYbyBxxwQA444ICUl5entLTFKQDAB9SltEsGf3fwtm4D2tRDFz60rVsAAABoV1pM3MePH5/p06dn5MiRLd501113tWlTAAAAAACwI2oxlJ8yZUqS5IYbbii0GQAAAAAA2JF1aGmwrKwsSXLrrbdmr7322ujfrbfeWmiDAAAAAACwo2gxlH/Hww8//K6xBQsWtFkzAAAAAACwI2vx+Jpbb701P/7xj7NkyZKUl5c3j69duzaHHnpoYc0BAAAAAMCOpMVQvry8PMccc0yuvfbaXHLJJc3j3bp1S8+ePQtrDgAAAAAAdiQthvI777xzdt5551x77bVpbGzMK6+8ksbGxqxbty7r1q3LnnvuWXSfAAAAAACw3WsxlH/Hf/zHf+S73/1uPvShD6VDh/87fv6uu+5q88YAAAAA2P7Ur69Pl9Iu27oNaDO+x/mgWg3lq6urc88992TXXXctqh8AAAAAtmNdSrtk8HcHb+s2oM08dOFD27oFtnMdWrvYp0+f7LzzzkX1AgAAAAAAm6WpqSlnnnlmHnzwweaxOXPm5LzzztuGXW1aqzvl+/btm7POOiuf+cxn0rlz5+bxsWPHtnljAAAAAADwXkpKSvIP//APGT9+fI466qg0NjZm2rRp+eEPf/iB6q5fvz6lpa1G5x9Iq5X33HPP7LnnnmloaEhDQ0ObNQEAAAAAAFtq//33z7HHHpt//dd/zbp16zJixIjss88+mTVrVm655ZY0NDTkE5/4RKZOnZoOHTrk8ssvz5NPPpn6+vqccMIJueCCC5IkxxxzTE4//fT87Gc/yznnnJMTTjihzXpuNZR/p6E/tX79+jZrBgAAAAAAtsQFF1yQkSNHpnPnzrnzzjvzhz/8Iffdd19uu+22lJaW5vLLL8/s2bNTXl6eSy65JD179sz69etz9tln5/jjj89+++2XJPmrv/qr3HbbbW3eb4tnyp955pnNrydOnLjRtdGjR7dtRwAAAAAAsJn+6q/+KieeeGJOPvnkdO7cOQ8//HB+85vfZNSoURkxYkT++7//Oy+88EKSZPbs2Rk5cmRGjhyZxYsX55lnnmmuc+KJJxbSb4s75d94443m13/84x83utbU1NS2HQEAAAAAwBbo0KFDOnT4vz3oo0aNykUXXbTRnP/5n//JzTffnDvuuCM9evTI3//936e+vr75+k477VRMry0NlpSUtPi6pa8BAAAAAKC9GDRoUO6+++6sXLkySbJq1ar87//+b9asWZNu3bqle/fuqaury89//vNt0l+LO+Vfe+213HfffdmwYUNee+21zJ07N8nbu+Rff/31QhsEAAAAAIDN9dGPfjQXXHBBxo4dmw0bNqRTp075+te/noMPPjj77rtvTjrppPTt2zeHHnroNumvxVD+yCOPzP3339/8+oEHHmi+dsQRRxTTGQAAAAAAbIYLL7xwo6/Ly8tTXl7+rnnf+ta3Wrx/wYIFbdJXS1oM5a+++urCGgAAAAAAgL8ULZ4pDwAAAAAAbH1CeQAAAAAAKEiLofzdd9+dJFmyZEmhzQAAAAAAwI6sxVC+qqoqSVJZWVloMwAAAAAAsCNr8UGvPXv2zFlnnZWlS5fmy1/+8ruu33DDDW3eGAAAAAAA7GhaDOV/8IMf5He/+10uvfTSnHvuuUX3BAAAAADADq6+oTFdOnUstN6LL76YSy+9NK+88ko6dOiQ0047Leecc05Wr16dCRMmZNmyZdlrr70ybdq07LLLLlm8eHEmT56cJ598MhMmTMh5552XJHn22WczYcKE5rpLlixJZWVlxowZs8k+WwzlO3funEMOOSS33XZbevXqlTVr1qSkpCTdunXbgv8CAAAAAABoWZdOHXPYxJu3Wr2F3zp7k3M6duyYSZMmpX///lmzZk1GjRqVwYMHZ+bMmRk0aFDGjRuXqqqqVFVVZeLEienZs2emTJmS+fPnb1SnX79+qa2tTZI0NjbmmGOOyec+97nN6rPFM+Xf8corr6SioiLl5eUZPnx4TjnllPzhD3/YrMIAAAAAANCelJWVpX///kmS7t27p1+/flm+fHnmz5+fioqKJElFRUXmzZuXJOndu3c+/vGPp7S0xf3tSZJHHnkkffv2zV577bVZPbx3pSRTp07NpEmTctRRRyVJHnvssUydOjW33XbbZhUHAAAAAID2aOnSpXnqqacyYMCArFixImVlZUneDu5Xrly52XVmz56dk046abPnt7pTft26dc2BfJIMHDgw69at2+ziAAAAAADQ3qxduzaVlZWZPHlyunfv/r7rvPXWW7n//vtz/PHHb/Y9rYbyffv2zXXXXZelS5dm6dKluf7667P33nu/7wYBAAAAAGBbamhoSGVlZcrLyzNs2LAkbx9TU1dXlySpq6tLr169NqvWggUL0r9//3zoQx/a7PVbDeWvuuqqrFq1KhdeeGEuvPDCrFq1KldfffVmFwcAAAAAgPaiqakpU6ZMSb9+/TJ27Njm8SFDhqSmpiZJUlNTk6FDh25WvdmzZ2f48OFb1EOrZ8rvsssuueyyy7aoIAAAAAAAbEp9Q2MWfuvsrVqvS6eOrc5ZuHBhamtrs//++2fEiBFJkosvvjjjxo3LRRddlBkzZmSPPfbI9OnTkyQvv/xyRo0alTVr1qRDhw6prq7OnDlz0r1797zxxht5+OGHc8UVV2xRn62G8u9XfX19vvCFL+Stt95KY2NjjjvuuFRWVmbJkiW5+OKL8+qrr+ZjH/tYrrnmmnTu3LktWgAAAAAAoB3bVIDeFvUOP/zwPP300y1eq66uftfYbrvtlgULFrQ4f6eddspjjz22ZU1mE8fXvF+dO3dOdXV1fvKTn6SmpiY/+9nP8qtf/Sr//M//nDFjxmTu3Lnp0aNHZsyY0RbLAwAAAABAu9RqKL9w4cLNGvtzJSUl6datW5Jk/fr1Wb9+fUpKSvLoo4/muOOOS5KMHDky8+fPfz89AwAAAADAdqnVUP6b3/zmZo21pLGxMSNGjMgnP/nJfPKTn0zfvn3To0ePlJa+fWJOnz59snz58vfRMgAAAAAAbJ9aPFN+0aJFWbRoUVauXJmbbrqpeXzNmjVpbGzcrMIdO3ZMbW1tXnvttfzd3/1dnn322XfNKSkpeZ9tAwAAAADA9qfFUL6hoSHr1q1LY2Nj1q5d2zzevXv3fOc739miBXr06JGBAwfmV7/6VV577bWsX78+paWleemll1JWVvbBugcAAAAAgO1Ii6H8kUcemSOPPDIjR47MXnvttcVFV65cmdLS0vTo0SNvvvlmHn744XzpS1/KwIEDc++992b48OGZNWtWhgwZ8oHfAAAAAAAAbC9aDOXf8dZbb+Xyyy/PsmXLsn79+ubxm2++udWidXV1mTRpUhobG9PU1JTjjz8+xx57bPbbb79MmDAh06ZNy4EHHpjRo0dvnXcBAAAAAMB2pWl9fUpKuxRa78UXX8yll16aV155JR06dMhpp52Wc845J6tXr86ECROybNmy7LXXXpk2bVp22WWXLF68OJMnT86TTz6ZCRMm5Lzzzmuu9aMf/Sh33HFHSkpKsv/+++fqq69Oly6bfj+thvLjx4/PGWeckdGjR6dDh1afCbuRAw44IDU1Ne8a79u3b2bMmLHZdQAAAAAA2DGVlHbJC1ccvNXq7TP1N5uc07Fjx0yaNCn9+/fPmjVrMmrUqAwePDgzZ87MoEGDMm7cuFRVVaWqqioTJ05Mz549M2XKlMyfP3+jOsuXL8/NN9+cOXPmpGvXrhk/fnxmz56dU045ZZM9tBrKl5aW5vOf//wmiwAAAAAAQHtXVlbW/KzT7t27p1+/flm+fHnmz5+ff//3f0+SVFRU5KyzzsrEiRPTu3fv9O7dOw8++OC7ajU2NubNN99MaWlp3nzzzc1+hmqr29+PPfbY3HLLLamrq8vq1aub/wEAAAAAwPZs6dKleeqppzJgwICsWLGiOVQvKyvLypUrW7139913z7nnnptjjz02n/rUp9K9e/d86lOf2qx1W90pP2vWrCTJjTfe2DxWUlLyrq36AAAAAACwvVi7dm0qKyszefLkdO/efYvvf/XVVzN//vzMnz8/O++8c8aPH5/a2tqMGDFik/e2Gsrff//9W9wMAAAAAAC0Vw0NDamsrEx5eXmGDRuWJOndu3fq6upSVlaWurq69OrVq9UaDz/8cPbee+/mecOGDcuiRYs+eCjf0sNak7fP1AEAAAAAgO1JU1NTpkyZkn79+mXs2LHN40OGDElNTU3GjRuXmpqaDB06tNU6e+65Z37961/njTfeSNeuXfPII4/koIMO2qweWg3lf/Ob/3tabX19fR555JH0799fKA8AAAAAwAfStL4++0z9zaYnbkG9ktIurc5ZuHBhamtrs//++zfvar/44oszbty4XHTRRZkxY0b22GOPTJ8+PUny8ssvZ9SoUVmzZk06dOiQ6urqzJkzJwMGDMhxxx2XkSNHprS0NAceeGBOP/30zeqz1VD+8ssv3+jr119/PRMnTtyswgAAAAAA8F42FaC3Rb3DDz88Tz/9dIvXqqur3zW22267ZcGCBS3Or6ysTGVl5ZY1maTDlkzu2rVrnn/++S1eBAAAAAAA2MRO+S9/+cvNrzds2JDFixfnhBNOaPOmAAAAAABgR9RqKH/uuec2v+7YsWP22muv9OnTp82bAgAAAACAHVGrx9cceeSR6devX9auXZvXXnstnTp1KqovAAAAAADY4bQays+ZMyejR4/OPffck7vvvrv5NQAAAAAAsOVaPb7mhhtuyIwZM9K7d+8kycqVKzNmzJgcf/zxhTQHAAAAAAA7klZ3yjc1NTUH8knSs2fPNDU1tXlTAAAAAADs2OrX1xde78UXX8xZZ52VE044IcOHD091dXWSZPXq1Rk7dmyGDRuWsWPH5tVXX02SLF68OKeffnoOOuig3HjjjRvVqq6uzkknnZThw4fnRz/60Wb32epO+U996lM577zzMnz48CRvH2dz9NFHb3ZxAAAAAABoSZfSLhn83cFbrd5DFz60yTkdO3bMpEmT0r9//6xZsyajRo3K4MGDM3PmzAwaNCjjxo1LVVVVqqqqMnHixPTs2TNTpkzJ/PnzN6rzhz/8IXfccUfuuOOOdOrUKeeff34+85nP5MMf/vAme2h1p/xXvvKVnH766Xn66afz+9//PqeffnouvfTSTRYFAAAAAID2pqysLP3790+SdO/ePf369cvy5cszf/78VFRUJEkqKioyb968JEnv3r3z8Y9/PKWlG+9vX7x4cQYMGJCddtoppaWlOeKII3LfffdtVg8t7pR//vnn88orr+Swww7LsGHDMmzYsCTJL37xi7zwwgvZZ5993t87BgAAAACAdmDp0qV56qmnMmDAgKxYsSJlZWVJ3g7uV65c2eq9+++/f6ZNm5ZVq1ala9euWbBgQQ466KDNWrfFnfJXXXVVunXr9q7xrl275qqrrtqswgAAAAAA0B6tXbs2lZWVmTx5crp3777F9++77745//zzc+655+b888/PRz/60XTs2HGz7m0xlF+2bFkOOOCAd40ffPDBWbZs2RY3CAAAAAAA7UFDQ0MqKytTXl7efEpM7969U1dXlySpq6tLr169Nlln9OjRmTVrVm655Zb07Nkzf/3Xf71Z67cYytfXv/dTat98883NKgwAAAAAAO1JU1NTpkyZkn79+mXs2LHN40OGDElNTU2SpKamJkOHDt1krRUrViRJ/vd//zdz587NSSedtFk9tHim/MEHH5zbb789p5122kbjd9xxR/Mh+AAAAAAA8H7Vr6/PQxc+tFXrdSnt0uqchQsXpra2Nvvvv39GjBiRJLn44oszbty4XHTRRZkxY0b22GOPTJ8+PUny8ssvZ9SoUVmzZk06dOiQ6urqzJkzJ927d8+FF16Y1atXp7S0NF/72teyyy67bFafLYbykydPzgUXXJC77rqrOYT/7W9/m4aGhnzve9/b7P8EAAAAAABoyaYC9Laod/jhh+fpp59u8Vp1dfW7xnbbbbcsWLCgxfm33nrrljX4/2sxlP/Qhz6U2267LY8++mj++Mc/Jkk+/elPZ9CgQe9rEQAAAAAA4D1C+XccddRROeqoo4rqBQAAAAAAdmgtPugVAAAAAADY+oTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQkK0eyr/44os566yzcsIJJ2T48OGprq5OkqxevTpjx47NsGHDMnbs2Lz66qtbe2kAAAAAAGjXtnoo37Fjx0yaNCl33313/vM//zO33nprnnnmmVRVVWXQoEGZO3duBg0alKqqqq29NAAAAAAAtGtbPZQvKytL//79kyTdu3dPv379snz58syfPz8VFRVJkoqKisybN29rLw0AAAAAAO1am54pv3Tp0jz11FMZMGBAVqxYkbKysiRvB/crV65sy6UBAAAAAKDdabNQfu3atamsrMzkyZPTvXv3tloGAAAAAAC2G20Syjc0NKSysjLl5eUZNmxYkqR3796pq6tLktTV1aVXr15tsTQAAAAAALRbWz2Ub2pqypQpU9KvX7+MHTu2eXzIkCGpqalJktTU1GTo0KFbe2kAAAAAAGjXSrd2wYULF6a2tjb7779/RowYkSS5+OKLM27cuFx00UWZMWNG9thjj0yfPn1rLw0AAAAAAO3aVg/lDz/88Dz99NMtXquurt7aywEAAAAAwHajzR70CgAAAAAAbEwoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABfZ9zOQAABINSURBVBHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABWmTUP6rX/1qBg0alJNOOql5bPXq1Rk7dmyGDRuWsWPH5tVXX22LpQEAAAAAoN1qk1D+lFNOyQ9/+MONxqqqqjJo0KDMnTs3gwYNSlVVVVssDQAAAAAA7VabhPJHHHFEdtlll43G5s+fn4qKiiRJRUVF5s2b1xZLAwAAAABAu1XYmfIrVqxIWVlZkqSsrCwrV64samkAAAAAAGgXPOgVAAAAAAAKUlgo37t379TV1SVJ6urq0qtXr6KWBgAAAACAdqGwUH7IkCGpqalJktTU1GTo0KFFLQ0AAAAAAO1Cm4TyF198cc4444w899xzOeaYY3LHHXdk3LhxeeihhzJs2LA89NBDGTduXFssDQAAAAAA7VZpWxS99tprWxyvrq5ui+UAAAAAAGC74EGvAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAURCgPAAAAAAAFEcoDAAAAAEBBhPIAAAAAAFAQoTwAAAAAABREKA8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAAAAAFEQoDwAAAAAABRHKAwAAAABAQYTyAAAAAABQEKE8AAAAAAAUpPBQfsGCBTnuuOPyuc99LlVVVUUvDwAAAAAA20yhoXxjY2OuuOKK/PCHP8zs2bPz05/+NM8880yRLQAAAAAAwDZTaCj/xBNP5K//+q/Tt2/fdO7cOcOHD8/8+fOLbAEAAAAAALaZkqampqaiFrvnnnvys5/9LFdeeWWSpKamJk888USmTp3a4vyBAwdmr732Kqo9AAAAAADeh1133TU33njjtm5ju1Ba5GIt5f8lJSXvOf+xxx5ry3YAAAAAAKBQhR5f06dPn7z00kvNXy9fvjxlZWVFtgAAAAAAANtMoaH8wQcfnP/5n//JkiVL8tZbb2X27NkZMmRIkS0AAAAAAMA2U+jxNaWlpZk6dWrOP//8NDY2ZtSoUfnIRz5SZAsAAAAAALDNFPqgVwAAAAAA+EtW6PE1AAAAAADwl0woDwAAAAAABRHKAxTgvvvuy0c/+tEsXry4eWzp0qU56aST2nTd6dOn5+GHH97s+U899VQefPDB5q+/+93v5sYbb9wqvTz22GP527/92za/BwCAtrFq1aqMGDEiI0aMyODBg3P00UdnxIgROfzww3PiiSe+r5pNTU0ZOHBgXn311SRJXV1dPvrRj+aXv/xl85yjjjoqq1ates8aM2fOzBVXXJEkmTRpUu655553zZkyZUqeeeaZ99XjnzvwwAMzYsSIDB8+PCeffHJuuummbNiwYavU3pqfvwFov4TyAAX46U9/msMOOyxz5swpdN3x48fnk5/85GbP//NQfltav379tm4BAIA/seuuu6a2tja1tbU544wzMmbMmNTW1qampiYdOry/eKGkpCQDBgzIr371qyTJokWL8rGPfSyLFi1Kkjz77LPZdddds+uuu36g3q+88srst99+H6jGO7p27Zra2trMnj07N910Ux588MF873vf2yq1AfjLIJQHaGNr167N448/niuvvDKzZ89ucU59fX2++tWvpry8PBUVFXn00UeTvL3r54ILLsh5552XYcOG5Zprrmm+5+c//3lOP/30jBw5MpWVlVm7du276v7pTqEhQ4bkO9/5TkaOHJny8vKNdu0nyVtvvZXvfOc7mTNnTkaMGNH8C4RnnnkmZ511VoYOHZqbb765eX5tbW1OPfXUjBgxIlOnTk1jY+O71l+wYEGOP/74nHnmmbnvvvuax5944omcccYZqaioyBlnnJFnn322+f1WVlbmy1/+cs4999yNaj3xxBOpqKjIkiVL3vs/GwCAbaKxsTGXXXZZhg8fnnPPPTdvvvlmkuSFF17Ieeedl1NOOSWf//zn3/UZNEkOPfTQPP7440neDuXHjBmzUUj/iU98Ikly//33Z/To0amoqMiYMWPyyiuvtNrTtGnTMmnSpGzYsCFnnXVWfvOb3yRJPvGJT+Rf/uVfcvLJJ+e0005rrvPCCy/ktNNOy6hRozJ9+vTmdVvTu3fvfOMb38gtt9ySpqamNDY25p/+6Z8yatSolJeX57bbbkvy9s8E55xzTvNn8Xnz5jXX+P73v5/jjjsuY8aMyXPPPbfJNQHY/gnlAdrYvHnzcvTRR+dv/uZv0rNnzzz55JPvmnPLLbckSe666658+9vfzqRJk1JfX5/k7d3r06ZNy1133ZW77747L774YlauXJnvf//7uemmmzJr1qwcdNBBuemmmzbZy6677ppZs2bljDPOyL/9279tdK1z586prKzMiSeemNra2uY/QX7uuedy44035o477sh1112XhoaGLF68OHfffXd+/OMfp7a2Nh06dMhdd921Ub36+vpcfvnlueGGG3Lrrbfm5Zdfbr7Wr1+//Md//EdqampSWVmZf/mXf2m+9qtf/Sr/+I//uNEvAB5//PF8/etfz/XXX5++fftu8n0CAFCs559/Pl/4whcye/bs7Lzzzrn33nuTJJdffnkuv/zyzJw5M1/5ylfyD//wD++69xOf+ETzzvgnnngin/3sZ/Piiy8meTuUP/TQQ5Mkhx12WG6//fbU1NRk+PDh+eEPf/ie/VxzzTVZuXJlrr766nft4l+3bl0GDBiQn/zkJzn88MNz++23J3l7N/3ZZ5+dO++8M2VlZZv93vv27ZsNGzZkxYoVmTFjRnbeeefceeedufPOO3P77bdnyZIl6dKlS6677rrMmjUr1dXV+ad/+qc0NTXlt7/9bebMmZOampp873vfa/7FAQA7ttJt3QDAjm727Nk555xzkiQnnnhifvrTn6Z///4bzVm4cGG++MUvJkn23Xff7Lnnns27ZAYNGpSdd965+dqyZcvy+uuv55lnnsmZZ56ZJGloaMghhxyyyV6GDRuWJDnooIM22rnemk9/+tPp3LlzevXqlV69emXFihV55JFH8tvf/jannnpqkuTNN99M7969N7rv2Wefzd57750Pf/jDSZKTTz65+Qee119/PV/5ylfy/PPPp6SkJA0NDc33DR48OD179mz+evHixZk6dWpuvPHG7L777pvVMwAAxdp7771z4IEHJkn69++fZcuWZe3atVm0aFHGjx/fPO+tt956170f//jH89RTT2XdunVZv359unXrlr59++b555/PokWLMnbs2CTJSy+9lAkTJuTll1/OW2+9lb333rvFXq6//voMGDAg3/jGN1q83qlTpxx77LFJ3v5c/NBDDyV5e3PIddddlyQpLy/f6K9UN6WpqSlJ8tBDD+Xpp59u/qXE66+/nueffz59+vTJtddem1/84hfp0KFDli9fnldeeSW//OUv89nPfjY77bRTkrf/uhWAHZ9QHqANrVq1Ko8++mj++Mc/pqSkJI2NjSkpKcmll1660bx3PsS3pHPnzs2vO3bsmMbGxjQ1NWXw4MG59tprt6ifTp06JUk6dOjQ4nEzm7P++vXr09TUlJEjR+aSSy5p9d6SkpIWx6dPn56BAwfmuuuuy9KlS3P22Wc3X3vnB5J37Lbbbqmvr89TTz0llAcAaKf+/DNjfX19mpqa0qNHj9TW1rZ670477ZR99tknd955Zz72sY8lSQ455JA8+OCDWbFiRfr165ck+eY3v5kxY8Zk6NCheeyxx97zHPeDDz44Tz75ZFavXr3RZo93dOrUqflz6pZ8Ln4vS5YsSceOHdO7d+80NTXlsssuy9FHH73RnJkzZ2blypWZOXNmOnXqlCFDhjT/Zex7fWYGYMfl+BqANnTvvfemoqIiDzzwQO6///48+OCD2XvvvbNw4cKN5h1xxBHNx78899xzefHFF5t/+GjJIYcckscffzzPP/98kuSNN97YKudPduvWrcWz6f/coEGDcu+992bFihVJktWrV2fZsmUbzenXr1+WLl2aF154IUk2Ok//9ddfbw7YZ82a1epaPXr0SFVVVa699to89thjW/R+AADYdrp375699947d999d5K3N6L8/ve/b3HuoYcemurq6ua//jzkkENy880355BDDmkOrf/0M2RNTc17rnv00UfnS1/6Uv72b/82a9as2ex+BwwYkLlz5ybJez4L6s+tXLkyX/va1/KFL3whJSUl+dSnPpUf//jHzX8J+txzz2XdunV5/fXX07t373Tq1CmPPvpo82fnI444Ivfdd1/efPPNrFmzJg888MBm9wvA9ksoD9CGZs+enc9+9rMbjQ0bNuxd569//vOfz4YNG1JeXp4JEybk6quv3mi30Z/r1atXrr766lx88cUpLy/Paaed1vyw1A9i4MCBeeaZZzZ60GtL9ttvv1x00UU599xzU15ennPPPXejM+OTpEuXLrniiisybty4nHnmmdlzzz2br51//vm59tprc8YZZ2zWzqQPfehDueGGG3LFFVfk17/+9ft/gwAAFOpb3/pWZsyYkZNPPjnDhw/f6AGnf+rQQw/NkiVLmh+u2r9//7z00ksbPWz1ggsuyPjx4/P5z3++xR3wf+qEE07I6NGj8//+3/9rfujspkyePDk33XRTTj311Lz88svp3r17i/PefPPNjBgxIsOHD8+YMWMyePDgXHDBBUmS0aNHZ7/99sspp5ySk046KVOnTk1jY2PKy8vz29/+Nqecckruuuuu5g04/fv3z4knnpgRI0aksrIyhx122Gb1CsD2raSptTMTAAAAAP4CvPHGG+natWtKSkoye/bs/PSnP833v//9bd0WADsgZ8oDAAAAf/GefPLJXHHFFc1n4V911VXbuiUAdlB2ygMAAAAAQEGcKQ8AAAAAAAURygMAAAAAQEGE8gAAAAAAUBChPAAAFGTevHl55plnmr+ePn16Hn744STJj370o7zxxhvbqjUAAKAgQnkAACjIn4fy48ePzyc/+ckkyc033yyUBwCAvwAlTU1NTdu6CQAA2F7V1tbm3//939PQ0JABAwbka1/7Wg4//PCcffbZeeCBB9K1a9dcf/31eeGFF/LlL3853bt3z84775zvfve7uf766/OZz3wmdXV1ueaaa/I3f/M36dmzZ04++eT88Y9/zOTJk5Mkt99++//Xzv18xKKGcQD/Nm7itGgRLVuMaBPDaNEsa5N+Ual2JUPaRkT/SZsiLaJFTEXapE36B9rOJiISiRIjc3eH4zrc0+3O3Ht8Psv3fT2eZ/v1eFOv17O9vd3maQEAgH/KpjwAAHxSvV7P+fl5Dg8PU6vVUigUcnp6mre3t5RKpZycnGR4eDhHR0cpl8sZGxvL1tZWarVa+vv7v9dZWVlJX19f9vf3c3BwkKmpqVxeXqbRaCRJjo+PMz8/364xAQCAL/RHuxsAAID/q5ubm9ze3mZhYSFJ8v7+nt7e3nR2dmZ0dDRJMjQ0lOvr61+q++3bt4yMjOTq6irFYjGNRiODg4Nf3j8AANB6QnkAAPikZrOZubm5bG5u/nC+t7eXjo6OJEmhUMjHx8cv115cXMzOzk6KxaIteQAA+I34vgYAAD6pUqnk4uIiT09PSZLn5+fc39//9H13d3deX1//1l2pVMrDw0POzs4yPT39tY0DAABtI5QHAIBPGhgYyMbGRqrVamZmZlKtVvP4+PjT95OTk9nd3c3s7Gzu7u5+uFtaWsra2lqWl5e/n01MTKRcLqenp+dfmwEAAGitjmaz2Wx3EwAAwF+tr69ndXU1lUql3a0AAABfxKY8AAD8x7y8vGR8fDxdXV0CeQAA+M3YlAcAAAAAgBaxKQ8AAAAAAC0ilAcAAAAAgBYRygMAAAAAQIv8CZcRocv0KdhrAAAAAElFTkSuQmCC\n",
      "text/plain": [
       "<Figure size 1498.38x360 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "with sns.axes_style('white'):\n",
    "    g = sns.catplot(\"entity\", data=entity_count, aspect=4.0, kind='count',\n",
    "                       hue='Year')\n",
    "    g.set_ylabels('Count of Entities')\n",
    "   "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "#sum entitys by entity name to get total revenue:\n",
    "entity_rev=df.groupby(['entity']).agg(total_revenue=pd.NamedAgg(column='totalrevenue', aggfunc=sum))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "entity_rev.reset_index(inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>entity</th>\n",
       "      <th>total_revenue</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>10302489</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>114246963</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "              entity  total_revenue\n",
       "0  Alone in the dark       10302489\n",
       "1   The Walking Dead      114246963"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "entity_rev"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [],
   "source": [
    "############################################################################################################"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [],
   "source": [
    "#double check:\n",
    "#get the total revenue for entity till now:\n",
    "AID_revenue = sum(df[df['entity'] == 'Alone in the dark']['totalrevenue'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The total revenue generated for alone in the dark is : $10302489\n"
     ]
    }
   ],
   "source": [
    "print (\"The total revenue generated for alone in the dark is : \" + \"$\"+ str(AID_revenue))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [],
   "source": [
    "#get the total revenue for entity till now:\n",
    "TWD_revenue = sum(df[df['entity'] == 'The Walking Dead']['totalrevenue'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The total revenue generated for The Walking Dead is : $114246963\n"
     ]
    }
   ],
   "source": [
    "print (\"The total revenue generated for The Walking Dead is : \" + \"$\"+ str(TWD_revenue))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [],
   "source": [
    "aitd_entity= df[df[\"entity\"] == 'Alone in the dark']\n",
    "twd_entity =df[df[\"entity\"] == 'The Walking Dead']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "def entity_revenue(entity):\n",
    "    revenue=entity.groupby(df['todate']).agg(total_revenue=pd.NamedAgg(column='totalrevenue', aggfunc=sum))\n",
    "                                            \n",
    "                            \n",
    "    revenue.reset_index(inplace=True)\n",
    "    return revenue\n",
    "\n",
    "\n",
    "        \n",
    "aid_revenue_df = entity_revenue(aitd_entity) \n",
    "twd_revenue_df = entity_revenue(twd_entity)\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>todate</th>\n",
       "      <th>total_revenue</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>2017-04-05</td>\n",
       "      <td>10485</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>2017-04-06</td>\n",
       "      <td>8388</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>2017-04-07</td>\n",
       "      <td>6990</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>2017-04-08</td>\n",
       "      <td>7184</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>2017-04-09</td>\n",
       "      <td>10679</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>870</td>\n",
       "      <td>2019-08-23</td>\n",
       "      <td>6789</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>871</td>\n",
       "      <td>2019-08-24</td>\n",
       "      <td>3396</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>872</td>\n",
       "      <td>2019-08-25</td>\n",
       "      <td>1798</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>873</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>799</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>874</td>\n",
       "      <td>2019-08-27</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>875 rows × 2 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "        todate  total_revenue\n",
       "0   2017-04-05          10485\n",
       "1   2017-04-06           8388\n",
       "2   2017-04-07           6990\n",
       "3   2017-04-08           7184\n",
       "4   2017-04-09          10679\n",
       "..         ...            ...\n",
       "870 2019-08-23           6789\n",
       "871 2019-08-24           3396\n",
       "872 2019-08-25           1798\n",
       "873 2019-08-26            799\n",
       "874 2019-08-27              0\n",
       "\n",
       "[875 rows x 2 columns]"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "aid_revenue_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [],
   "source": [
    "###visualization:\n",
    "def plotting(data):\n",
    "    fig = plt.figure(figsize =(60,15))\n",
    "    return sns.barplot(x ='todate', y = 'total_revenue', data=data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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AAAAAMwNoTgAAAAAAAAAAAAAAAAA5oZQHAAAAAAAAAAAAAAAAABzQygOAAAAAAAAAAAAAAAAgLkhFAcAAAAAAAAAAAAAAADA3BCKAwAAAAAAAAAAAAAAAGBuCMUBAAAAAAAAAAAAAAAAMDeE4gAAAAAAAAAAAAAAAACYG0JxAAAAAAAAAAAAAAAAAMwNoTgAAAAAAAAAAAAAAAAA5oZQHAAAAAAAAAAAAAAAAABzQygOAAAAAAAAAAAAAAAAgLkhFAcAAAAAAAAAAAAAAADA3BCKAwAAAAAAAAAAAAAAAGBuCMUBAAAAAAAAAAAAAAAAMDeE4gAAAAAAAAAAAAAAAACYG0JxAAAAAAAAAAAAAAAAAMwNoTgAAAAAAAAAAAAAAAAA5oZQHAAAAAAAAAAAAAAAAABzQygOAAAAAAAAAAAAAAAAgLkhFAcAAAAAAAAAAAAAAADA3BCKAwAAAAAAAAAAAAAAAGBuCMUBAAAAAAAAAAAAAAAAMDeE4gAAAAAAAAAAAAAAAACYG0JxAAAAAAAAAAAAAAAAAMwNoTgAAAAAAAAAAAAAAAAA5oZQHAAAAAAAAAAAAAAAAABzQygOAAAAAAAAAAAAAAAAgLkhFAcAAAAAAAAAAAAAAADA3BCKAwAAAAAAAAAAAAAAAGBuCMUBAAAAAAAAAAAAAAAAMDeE4gAAAAAAAAAAAAAAAACYG0JxAAAAAAAAAAAAAAAAAMwNoTgAAAAAAAAAAAAAAAAA5oZQHAAAAAAAAAAAAAAAAABzQygOAAAAAAAAAAAAAAAAgLkhFAcAAAAAAAAAAAAAAADA3BCKAwAAAAAAAAAAAAAAAGBuCMUBAAAAAAAAAAAAAAAAMDeE4gAAAAAAAAAAAAAAAACYG0JxAAAAAAAAAAAAAAAAAMwNoTgAAAAAAAAAAAAAAAAA5oZQHAAAAAAAAAAAAAAAAABzQygOAAAAAAAAAAAAAAAAgLkhFAcAAAAAAAAAAAAAAADA3BCKAwAAAAAAAAAAAAAAAGBuCMUBAAAAAAAAAAAAAAAAMDeE4gAAAAAAAAAAAAAAAACYG0JxAAAAAAAAAAAAAAAAAMwNoTgAAAAAAAAAAAAAAAAA5oZQHAAAAAAAAAAAAAAAAABzQygOAAAAAAAAAAAAAAAAgLkhFAcAAAAAAAAAAAAAAADA3BCKAwAAAAAAAAAAAAAAAGBu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\n",
      "text/plain": [
       "<Figure size 4320x1080 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    },
    {
     "data": {
      "image/png": "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TwIAAAAAwDOBN8UBAAAAAAAAAAAAAAAAMIYoDgAAAAAAAAAAAAAAAIAxRHEAAAAAAAAAAAAAAAAAjCGKAwAAAAAAAAAAAAAAAGAMURwAAAAAAAAAAAAAAAAAY4jiAAAAAAAAAAAAAAAAABhDFAcAAAAAAAAAAAAAAADAGKI4AAAAAAAAAAAAAAAAAMYQxQEAAAAAAAAAAAAAAAAwhigOAAAAAAAAAAAAAAAAgDFEcQAAAAAAAAAAAAAAAACMIYoDAAAAAAAAAAAAAAAAYAxRHAAAAAAAAAAAAAAAAABjiOIAAAAAAAAAAAAAAAAAGEMUBwAAAAAAAAAAAAAAAMAYojgAAAAAAAAAAAAAAAAAxhDFAQAAAAAAAAAAAAAAADCGKA4AAAAAAAAAAAAAAACAMURxAAAAAAAAAAAAAAAAAIwhigMAAAAAAAAAAAAAAABgDFEcAAAAAAAAAAAAAAAAAGOI4gAAAAAAAAAAAAAAAAAYQxQHAAAAAAAAAAAAAAAAwBiiOAAAAAAAAAAAAAAAAADGEMUBAAAAAAAAAAAAAAAAMIYoDgAAAAAAAAAAAAAAAIAxRHEAAAAAAAAAAAAAAAAAjCGKAwAAAAAAAAAAAAAAAGAMURwAAAAAAAAAAAAAAAAAY4jiAAAAAAAAAAAAAAAAABhDFAcAAAAAAAAAAAAAAADAGKI4AAAAAAAAAAAAAAAAAMYQxQEAAAAAAAAAAAAAAAAwhigOAAAAAAAAAAAAAAAAgDFEcQAAAAAAAAAAAAAAAACMIYoDAAAAAAAAAAAAAAAAYAxRHAAAAAAAAAAAAAAAAABjiOIAAAAAAAAAAAAAAAAAGEMUBwAAAAAAAAAAAAAAAMAYojgAAAAAAAAAAAAAAAAAxhDFAQAAAAAAAAAAAAAAADCGKA4AAAAAAAAAAAAAAACAMURxAAAAAAAAAAAAAAAAAIwhigMAAAAAAAAAAAAAAABgDFEcAAAAAAAAAAAAAAAAAGOI4gAAAAAAAAAAAAAAAAAYQxQHAAAAAAAAAAAAAAAAwBiiOAAAAAAAAAAAAAAAAADGEMUBAAAAAAAAAAAAAAAAMIYoDgAAAAAAAAAAAAAAAIAxRHEAAAAAAAAAAAAAAAAAjCGKAwAAAAAAAAAAAAAAAGAMURwAAAAAAAAAAAAAAAAAY4jiAAAAAAAAAAAAAAAAABhDFAcAAAAA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\n",
      "text/plain": [
       "<Figure size 4320x1080 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "aid_revenue_plots = plotting(aid_revenue_df).set_title(('Alone in the Dark: date vs Revenue'),fontsize ='32')\n",
    "twd_revenue_plots = plotting(twd_revenue_df).set_title(('The Waling Dead: date vs Revenue'),fontsize ='32')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [],
   "source": [
    "def entity_yearly_revenue(entity):\n",
    "    \n",
    "    monthly_revenue=entity.groupby([df['todate'].dt.month.rename(\"Month\"), df['todate'].dt.year.rename(\"Year\")]).agg(total_revenue=pd.NamedAgg(column='totalrevenue', aggfunc=sum))\n",
    "    monthly_revenue.reset_index(inplace=True)\n",
    "    return monthly_revenue"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "aitd_yearly_revenue = entity_yearly_revenue(aitd_entity)\n",
    "twd_yearly_revenue = entity_yearly_revenue(twd_entity)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Month</th>\n",
       "      <th>Year</th>\n",
       "      <th>total_revenue</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>2018</td>\n",
       "      <td>3980970</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>2019</td>\n",
       "      <td>3548196</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>2</td>\n",
       "      <td>2018</td>\n",
       "      <td>2423736</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>2</td>\n",
       "      <td>2019</td>\n",
       "      <td>2403619</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>3</td>\n",
       "      <td>2018</td>\n",
       "      <td>2696352</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>5</td>\n",
       "      <td>3</td>\n",
       "      <td>2019</td>\n",
       "      <td>2525323</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6</td>\n",
       "      <td>4</td>\n",
       "      <td>2017</td>\n",
       "      <td>1432421</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>7</td>\n",
       "      <td>4</td>\n",
       "      <td>2018</td>\n",
       "      <td>3051896</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>8</td>\n",
       "      <td>4</td>\n",
       "      <td>2019</td>\n",
       "      <td>3084518</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>9</td>\n",
       "      <td>5</td>\n",
       "      <td>2017</td>\n",
       "      <td>2667192</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>10</td>\n",
       "      <td>5</td>\n",
       "      <td>2018</td>\n",
       "      <td>3096130</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>11</td>\n",
       "      <td>5</td>\n",
       "      <td>2019</td>\n",
       "      <td>2784837</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>12</td>\n",
       "      <td>6</td>\n",
       "      <td>2017</td>\n",
       "      <td>4721700</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>13</td>\n",
       "      <td>6</td>\n",
       "      <td>2018</td>\n",
       "      <td>5645036</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>14</td>\n",
       "      <td>6</td>\n",
       "      <td>2019</td>\n",
       "      <td>4620323</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>15</td>\n",
       "      <td>7</td>\n",
       "      <td>2017</td>\n",
       "      <td>5244003</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>16</td>\n",
       "      <td>7</td>\n",
       "      <td>2018</td>\n",
       "      <td>7023363</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>17</td>\n",
       "      <td>7</td>\n",
       "      <td>2019</td>\n",
       "      <td>6108617</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>18</td>\n",
       "      <td>8</td>\n",
       "      <td>2017</td>\n",
       "      <td>5751936</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>19</td>\n",
       "      <td>8</td>\n",
       "      <td>2018</td>\n",
       "      <td>8826248</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>20</td>\n",
       "      <td>8</td>\n",
       "      <td>2019</td>\n",
       "      <td>5474223</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>21</td>\n",
       "      <td>9</td>\n",
       "      <td>2017</td>\n",
       "      <td>3647236</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>22</td>\n",
       "      <td>9</td>\n",
       "      <td>2018</td>\n",
       "      <td>6035197</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>23</td>\n",
       "      <td>10</td>\n",
       "      <td>2017</td>\n",
       "      <td>3191286</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>24</td>\n",
       "      <td>10</td>\n",
       "      <td>2018</td>\n",
       "      <td>4503276</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>25</td>\n",
       "      <td>11</td>\n",
       "      <td>2017</td>\n",
       "      <td>2711424</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>26</td>\n",
       "      <td>11</td>\n",
       "      <td>2018</td>\n",
       "      <td>3004790</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>27</td>\n",
       "      <td>12</td>\n",
       "      <td>2017</td>\n",
       "      <td>1952566</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>28</td>\n",
       "      <td>12</td>\n",
       "      <td>2018</td>\n",
       "      <td>2090549</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    Month  Year  total_revenue\n",
       "0       1  2018        3980970\n",
       "1       1  2019        3548196\n",
       "2       2  2018        2423736\n",
       "3       2  2019        2403619\n",
       "4       3  2018        2696352\n",
       "5       3  2019        2525323\n",
       "6       4  2017        1432421\n",
       "7       4  2018        3051896\n",
       "8       4  2019        3084518\n",
       "9       5  2017        2667192\n",
       "10      5  2018        3096130\n",
       "11      5  2019        2784837\n",
       "12      6  2017        4721700\n",
       "13      6  2018        5645036\n",
       "14      6  2019        4620323\n",
       "15      7  2017        5244003\n",
       "16      7  2018        7023363\n",
       "17      7  2019        6108617\n",
       "18      8  2017        5751936\n",
       "19      8  2018        8826248\n",
       "20      8  2019        5474223\n",
       "21      9  2017        3647236\n",
       "22      9  2018        6035197\n",
       "23     10  2017        3191286\n",
       "24     10  2018        4503276\n",
       "25     11  2017        2711424\n",
       "26     11  2018        3004790\n",
       "27     12  2017        1952566\n",
       "28     12  2018        2090549"
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "twd_yearly_revenue "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [],
   "source": [
    "def plotting_yearly_rev(data):\n",
    "    fig = plt.figure(figsize =(50,15))\n",
    "    return sns.barplot(x ='Year', y = 'total_revenue', data=data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "data": {
      "image/png": "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AKBCvAwAAAAAAAAAAAAAVIiXAQAAAAAAAAAAAIAK8TIAAAAAAAAAAAAAUCFeBgAAAAAAAAAAAAAqxMsAAAAAAAAAAAAAQIV4GQAAAAAAAAAAAACoEC8DAAAAAAAAAAAAABXiZQAAAAAAAAAAAACgQrwMAAAAAAAAAAAAAFSIlwEAAAAAAAAAAACACvEyAAAAAAAAAAAAAFAhXgYAAAAAAAAAAAAAKsTLAAAAAAAAAAAAAECFeBkAAAAAAAAAAAAAqBAvAwAAAAAAAAAAAAAV4mUAAAAAAAAAAAAAoEK8DAAAAAAAAAAAAABUiJcBAAAAAAAAAAAAgArxMgAAAAAAAAAAAABQIV4GAAAAAAAAAAAAACrEywAAAAAAAAAAAABAhXgZAAAAAAAAAAAAAKgQLwMAAAAAAAAAAAAAFeJlAAAAAAAAAAAAAKBCvAwAAAAAAAAAAAAAVIiXAQAAAAAAAAAAAIAK8TIAAAAAAAAAAAAAUCFeBgAAAAAAAAAAAAAqxMsAAAAAAAAAAAAAQIV4GQAAAAAAAAAAAACoEC8DAAAAAAAAAAAAABXiZQAAAAAAAAAAAACgQrwMAAAAAAAAAAAAAFSIlwEAAAAAAAAAAACACvEyAAAAAAAAAAAAAFAhXgYAAAAAAAAAAAAAKsTLAAAAAAAAAAAAAECFeBkAAAAAAAAAAAAAqBAvAwAAAAAAAAAAAAAV4mUAAAAAAAAAAAAAoEK8DAAAAAAAAAAAAABUiJcBAAAAAAAAAAAAgArxMgAAAAAAAAAAAABQIV4GAAAAAAAAAAAAACrEywAAAAAAAAAAAABAhXgZAAAAAAAAAAAAAKgQLwMAAAAAAAAAAAAAFeJlAAAAAAAAAAAAAKBCvAwAAAAAAAAAAAAAVIiXAQAAAAAAAAAAAIAK8TIAAAAAAAAAAAAAUCFeBgAAAAAAAAAAAAAqxMsAAAAAAAAAAAAAQIV4GQAAAAAAAAAAAACoEC8DAAAAAAAAAAAAABXiZQAAAAAAAAAAAACgQrwMAAAAAAAAAAAAAFSIlwEAAAAAAAAAAACACvEyAAAAAAAAAAAAAFAhXgYAAAAAAAAAAAAAKsTLAAAAAAAAAAAAAECFeBkAAAAAAAAAAAAAqBAvAwAAAAAAAAAAAAAV4mUAAAAAAAAAAAAAoEK8DAAAAAAAAAAAAABUiJcBAAAAAAAAAAAA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AIAK8TIAAAAAAAAAAAAAUCFeBgAAAAAAAAAAAAAqxMsAAAAAAAAAAAAAQIV4GQAAAAAAAAAAAACoEC8DAAAAAAAAAAAAABXiZQAAAAAAAAAAAACgQrwMAAAAAAAAAAAAAFSIlwEAAAAAAAAAAACACvEyAAAAAAAAAAAAAFAhXgYAAAAAAAAAAAAAKsTLAAAAAAAAAAAAAECFeBkAAAAAAAAAAAAAqBAvAwAAAAAAAAAAAAAV4mUAAAAAAAAAAAAAoEK8DAAAAAAAAAAAAABUiJcBAAAAAAAAAAAAgArxMgAAAAAAAAAAAABQIV4GAAAAAAAAAAAAACrEywAAAAAAAAAAAABAhXgZAAAAAAAAAAAAAKgQLwMAAAAAAAAAAAAAFeJlAAAAAAAAAAAAAKBCvAwAAAAAAAAAAAAAVIiXAQAAAAAAAAAAAIAK8TIAAAAAAAAAAAAAUCFeBgAAAAAAAAAAAAAqxMsAAAAAAAAAAAAAQIV4GQAAAAAAAAAAAACoEC8DAAAAAAAAAAAAABXiZQAAAAAAAAAAAACgQrwMAAAAAAAAAAAAAFSIlwEAAAAAAAAAAACACvEyAAAAAAAAAAAAAFAhXgYAAAAAAAAAAAAAKsTLAAAAAAAAAAAAAECFeBkAAAAAAAAAAAAAqBAvAwAAAAAAAAAAAAAV4mUAAAAAAAAAAAAAoEK8DAAAAAAAAAAAAABUiJcBAAAAAAAAAAAAgArxMgAAAAAAAAAAAABQIV4GAAAAAAAAAAAAACrEywAAAAAAAAAAAABAhXgZAAAAAAAAAAAAAKgQLwMAAAAAAAAAAAAAFeJlAAAAAAAAAAAAAKBCvAwAAAAAAAAAAAAAVIiXAQAAAAAAAAAAAIAK8TIAAAAAAAAAAAAAUCFeBgAAAAAAAAAAAAAqxMsAAAAAAAAAAAAAQIV4GQAAAAAAAAAAAACoEC8DAAAAAAAAAAAAABXiZQAAAAAAAAAAAACgQrwMAAAAAAAAAAAAAFSIlwEAAAAAAAAAAACACvEyAAAAAAAAAAAAAFAhXgYAAAAAAAAAAAAAKsTLAAAAAAAAAAAAAECFeBkAAAAAAAAAAAAAqBAvAwAAAAAAAAAAAAAV4mUAAAAAAAAAAAAAoEK8DAAAAAAAAAAAAABUiJcBAAAAAAAAAAAAgArxMgAAAAAAAAAAAABQIV4GAAAAAAAAAAAAACrEywAAAAAAAAAAAABAhXgZAAAAAAAAAAAAAKgQLwMAAAAAAAAAAAAAFeJlAAAAAAAAAAAAAKBCvAwAAAAAAAAAAAAAVIiXAQAAAAAAAAAAAIAK8TIAAAAAAAAAAAAAUCFeBgAAAAAAAAAAAAAqxMsAAAAAAAAAAAAAQMUdHS/PzNmZ+fbMXJ6ZJ/d9HgAAAAAAAAAAAAC4m92x8fLM/FqSv0zyaJIHknxyZh7Y76kAAAAAAAAAAAAA4O51x8bLSR5Mcnmt9R9rrf9K8rdJHtvzmQAAAAAAAAAAAADgrjVrrX2f4UjMzO8nObvW+oPt86eSPLTW+sOb1p1Pcn77+NtJvl09KADcGd6X5D/3fQgAAADuGr6HAgAA0OR7KADcnt9ca524eXjPPk5SMjtmv1Rqr7WeTfLs0R8HAO5cM3NprXV63+cAAADg7uB7KAAAAE2+hwLA/65j+z7AEbqS5L4Dn08leX1PZwEA4Oft3V+on3UdB/D3ZzsNnSWsxeoorgykGt4oZWHhjULaRWWQTQgW1EWRMIsgCbpY3VRIdJugJFRrroS8iJWGhPZHXMtwcxfDIs2GBis3V8yNfbo4T3Bobm2c5/x+58/rBT9+P57ny5f39/JznjfPAQAAAAAAAABg1VvJ5eUnk1xVVVdW1bokW5M8NOVMAAAAAAAAAAAAALBqzUw7wGLp7lNVdUeSnydZm+S+7j4w5VgAsFLdM+0AAAAArCrmUAAAACbJHAoAI6runnYGAAAAAAAAAAAAAGAVWDPtAAAAAAAAAAAAAADA6qC8DAAAAAAAAAAAAABMhPIyAHCGqrqiqh6tqoNVdaCqtg/X31hVD1fVoeF7w3D9nVX126o6UVVfmrfPO6rqqXmfo1V157TOBQAAwNI01hw63PvCsMf+qtpZVRdN40wAAAAsXSPPoduHGfSAZ6EAcH6qu6edAQBYYqpqNslsd++rqjck+X2Sjyb5VJIj3f2NqroryYbu/nJVbUry1mHNP7r77tfYc22SF5K8t7v/MqmzAAAAsPSNNYdW1eVJHk+ypbv/XVUPJPlZd39v8qcCAABgqRpxDr06yY+SXJfk1SR7knyuuw9N/FAAsIx48zIAcIbuPtzd+4bfx5IcTHJ5ko8kuX9Ydn/mhvN090vd/WSSk+fY9sYkzyouAwAA8L9GnkNnklxcVTNJ1if52yLHBwAAYJkZcQ59V5Lfdfe/uvtUkl8luXUCRwCAZU15GQA4p6p6W5JrkjyR5M3dfTiZG+iTbLqArbYm2Tl2PgAAAFaWhcyh3f1CkruTPJfkcJKXu/sXi5kXAACA5W2Bz0P3J7mhqjZW1fokH0pyxeKlBYCVQXkZADirqnp9kp8kubO7jy5gn3VJPpxk91jZAAAAWHkWOodW1YbMvSXryiSXJbmkqj45bkoAAABWioXOod19MMk3kzycZE+SPyY5NWpIAFiBlJcBgNdUVa/L3KD+g+5+cLj8YlXNDvdnk7x0ntvdkmRfd784flIAAABWgpHm0JuS/Lm7/97dJ5M8mOT6xcoMAADA8jXW89Duvre7r+3uG5IcSXJosTIDwEqhvAwAnKGqKsm9SQ5297fn3Xooybbh97YkPz3PLW9PsnO8hAAAAKwkI86hzyV5X1WtH/a8McnBsfMCAACwvI35PLSqNg3fm5N8LJ6LAsD/Vd097QwAwBJTVR9I8liSp5OcHi5/JckTSR5IsjlzD4Q/3t1HquotSfYmuXRY/0qSLd19tKrWJ3k+ydu7++XJngQAAIDlYOQ5dEeST2Tu3/T+Iclnuvsxs4kxAAACjUlEQVTEJM8DAADA0jbyHPpYko1JTib5Ynf/cqKHAYBlSHkZAAAAAAAAAAAAAJiINdMOAAAAAAAAAAAAAACsDsrLAAAAAAAAAAAAAMBEKC8DAAAAAAAAAAAAABOhvAwAAAAAAAAAAAAATITyMgAAAAAAAAAAAAAwEcrLAAAAAABMVc15vKpumXfttqraM81cAAAAAACMr7p72hkAAAAAAFjlqurqJLuTXJNkbZKnktzc3c8uYM+Z7j41UkQAAAAAAEagvAwAAAAAwJJQVd9KcjzJJUmOdffXq2pbks8nWZfkN0nu6O7TVXVPkmuTXJxkV3d/bdjjr0m+m+TmJN/p7t1TOAoAAAAAAGcxM+0AAAAAAAAw2JFkX5JXk7x7eBvzrUmu7+5TQ2F5a5IfJrmru49U1UySR6vqx939zLDP8e5+/zQOAAAAAADAuSkvAwAAAACwJHT38araleSV7j5RVTcleU+SvVWVzL1l+flh+e1V9enM/Z37siRbkvy3vLxrsskBAAAAADhfyssAAAAAACwlp4dPklSS+7r7q/MXVNVVSbYnua67/1lV309y0bwlxyeSFAAAAACAC7Zm2gEAAAAAAOAsHklyW1W9KUmqamNVbU5yaZJjSY5W1WySD04xIwAAAAAAF8CblwEAAAAAWJK6++mq2pHkkapak+Rkks8m2ZvkmST7k/wpya+nlxIAAAAAgAtR3T3tDAAAAAAAAAAAAADAKrBm2gEAAAAAAAAAAAAAgNVBeRkAAAAAAAAAAAAAmAjlZQAAAAAAAAAAAABgIpSXAQAAAAAAAAAAAICJUF4GAAAAAAAAAAAAACZCeRkAAAAAAAAAAAAAmAjlZQAAAAAAAAAAAABgIv4Dj7UJI1/FqUoAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 3600x1080 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 3600x1080 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "aitd_yearly_rev_plots = plotting_yearly_rev(aitd_yearly_revenue).set_title(('Alone in the Dark: Year vs Revenue'),fontsize ='32')\n",
    "twd_yearly_rev_plots = plotting_yearly_rev(twd_yearly_revenue).set_title(('The Waling Dead: Year vs Revenue'),fontsize ='32')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Time Series Modeling using LSTM-Keras-Tensorflow"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_ts = df.copy()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Considering only Data from Simon & Schuster as PublishingParent to predict future revenues:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_ts=df_ts[df_ts['publisherparent'].str.contains(\"Simon & Schuster\")]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DatetimeIndex(['2017-04-19', '2017-04-20', '2017-04-21', '2017-04-22',\n",
       "               '2017-04-23', '2017-04-24', '2017-04-25', '2017-04-26',\n",
       "               '2017-04-27', '2017-04-28',\n",
       "               ...\n",
       "               '2019-08-18', '2019-08-19', '2019-08-20', '2019-08-21',\n",
       "               '2019-08-22', '2019-08-23', '2019-08-24', '2019-08-25',\n",
       "               '2019-08-26', '2019-08-27'],\n",
       "              dtype='datetime64[ns]', name='todate', length=6527, freq=None)"
      ]
     },
     "execution_count": 49,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_ts =df_ts.set_index('todate')\n",
    "df_ts.index"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>entity</th>\n",
       "      <th>formattype</th>\n",
       "      <th>fromdate</th>\n",
       "      <th>titlecount</th>\n",
       "      <th>titles</th>\n",
       "      <th>author</th>\n",
       "      <th>amazontotalreviews</th>\n",
       "      <th>minappleprice</th>\n",
       "      <th>amazontotalrevenue</th>\n",
       "      <th>accruedpreordersoldunits</th>\n",
       "      <th>...</th>\n",
       "      <th>lumpedpreorderrevenue</th>\n",
       "      <th>amazonsoldunits</th>\n",
       "      <th>amazonpreordersubscriptionrevenue</th>\n",
       "      <th>preordersubscriptionunits</th>\n",
       "      <th>amazonpreordersalesrevenue</th>\n",
       "      <th>maxappleprice</th>\n",
       "      <th>pagelength</th>\n",
       "      <th>pricewassetbypublisher</th>\n",
       "      <th>barnesandnobledistributor</th>\n",
       "      <th>appledistributor</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>todate</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>2017-04-19</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-18</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2017-04-20</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-19</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306</td>\n",
       "      <td>0</td>\n",
       "      <td>702</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2017-04-21</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-20</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306</td>\n",
       "      <td>0</td>\n",
       "      <td>4914</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2017-04-22</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-21</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306</td>\n",
       "      <td>0</td>\n",
       "      <td>4212</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2017-04-23</td>\n",
       "      <td>Alone in the dark</td>\n",
       "      <td>print</td>\n",
       "      <td>2017-04-22</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 306, 'minappleprice': 0...</td>\n",
       "      <td>Frith Banbury</td>\n",
       "      <td>306</td>\n",
       "      <td>0</td>\n",
       "      <td>702</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2019-08-23</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-22</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275</td>\n",
       "      <td>0</td>\n",
       "      <td>81835</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>25</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2019-08-24</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-23</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275</td>\n",
       "      <td>0</td>\n",
       "      <td>18460</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2019-08-25</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-24</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275</td>\n",
       "      <td>0</td>\n",
       "      <td>38623</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>12</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-25</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275</td>\n",
       "      <td>0</td>\n",
       "      <td>80340</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>25</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2019-08-27</td>\n",
       "      <td>The Walking Dead</td>\n",
       "      <td>audio</td>\n",
       "      <td>2019-08-26</td>\n",
       "      <td>1</td>\n",
       "      <td>{'amazontotalreviews': 275, 'minappleprice': 0...</td>\n",
       "      <td>Matthew Murdock</td>\n",
       "      <td>275</td>\n",
       "      <td>0</td>\n",
       "      <td>43212</td>\n",
       "      <td>0</td>\n",
       "      <td>...</td>\n",
       "      <td>0</td>\n",
       "      <td>13</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>395.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>6527 rows × 105 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                       entity formattype   fromdate  titlecount  \\\n",
       "todate                                                            \n",
       "2017-04-19  Alone in the dark      print 2017-04-18           1   \n",
       "2017-04-20  Alone in the dark      print 2017-04-19           1   \n",
       "2017-04-21  Alone in the dark      print 2017-04-20           1   \n",
       "2017-04-22  Alone in the dark      print 2017-04-21           1   \n",
       "2017-04-23  Alone in the dark      print 2017-04-22           1   \n",
       "...                       ...        ...        ...         ...   \n",
       "2019-08-23   The Walking Dead      audio 2019-08-22           1   \n",
       "2019-08-24   The Walking Dead      audio 2019-08-23           1   \n",
       "2019-08-25   The Walking Dead      audio 2019-08-24           1   \n",
       "2019-08-26   The Walking Dead      audio 2019-08-25           1   \n",
       "2019-08-27   The Walking Dead      audio 2019-08-26           1   \n",
       "\n",
       "                                                       titles  \\\n",
       "todate                                                          \n",
       "2017-04-19  {'amazontotalreviews': 306, 'minappleprice': 0...   \n",
       "2017-04-20  {'amazontotalreviews': 306, 'minappleprice': 0...   \n",
       "2017-04-21  {'amazontotalreviews': 306, 'minappleprice': 0...   \n",
       "2017-04-22  {'amazontotalreviews': 306, 'minappleprice': 0...   \n",
       "2017-04-23  {'amazontotalreviews': 306, 'minappleprice': 0...   \n",
       "...                                                       ...   \n",
       "2019-08-23  {'amazontotalreviews': 275, 'minappleprice': 0...   \n",
       "2019-08-24  {'amazontotalreviews': 275, 'minappleprice': 0...   \n",
       "2019-08-25  {'amazontotalreviews': 275, 'minappleprice': 0...   \n",
       "2019-08-26  {'amazontotalreviews': 275, 'minappleprice': 0...   \n",
       "2019-08-27  {'amazontotalreviews': 275, 'minappleprice': 0...   \n",
       "\n",
       "                     author  amazontotalreviews  minappleprice  \\\n",
       "todate                                                           \n",
       "2017-04-19    Frith Banbury                 306              0   \n",
       "2017-04-20    Frith Banbury                 306              0   \n",
       "2017-04-21    Frith Banbury                 306              0   \n",
       "2017-04-22    Frith Banbury                 306              0   \n",
       "2017-04-23    Frith Banbury                 306              0   \n",
       "...                     ...                 ...            ...   \n",
       "2019-08-23  Matthew Murdock                 275              0   \n",
       "2019-08-24  Matthew Murdock                 275              0   \n",
       "2019-08-25  Matthew Murdock                 275              0   \n",
       "2019-08-26  Matthew Murdock                 275              0   \n",
       "2019-08-27  Matthew Murdock                 275              0   \n",
       "\n",
       "            amazontotalrevenue  accruedpreordersoldunits  ...  \\\n",
       "todate                                                    ...   \n",
       "2017-04-19                   0                         0  ...   \n",
       "2017-04-20                 702                         0  ...   \n",
       "2017-04-21                4914                         0  ...   \n",
       "2017-04-22                4212                         0  ...   \n",
       "2017-04-23                 702                         0  ...   \n",
       "...                        ...                       ...  ...   \n",
       "2019-08-23               81835                         0  ...   \n",
       "2019-08-24               18460                         0  ...   \n",
       "2019-08-25               38623                         0  ...   \n",
       "2019-08-26               80340                         0  ...   \n",
       "2019-08-27               43212                         0  ...   \n",
       "\n",
       "            lumpedpreorderrevenue  amazonsoldunits  \\\n",
       "todate                                               \n",
       "2017-04-19                      0                6   \n",
       "2017-04-20                      0                7   \n",
       "2017-04-21                      0                7   \n",
       "2017-04-22                      0                6   \n",
       "2017-04-23                      0                1   \n",
       "...                           ...              ...   \n",
       "2019-08-23                      0               25   \n",
       "2019-08-24                      0                5   \n",
       "2019-08-25                      0               12   \n",
       "2019-08-26                      0               25   \n",
       "2019-08-27                      0               13   \n",
       "\n",
       "            amazonpreordersubscriptionrevenue  preordersubscriptionunits  \\\n",
       "todate                                                                     \n",
       "2017-04-19                                  0                          0   \n",
       "2017-04-20                                  0                          0   \n",
       "2017-04-21                                  0                          0   \n",
       "2017-04-22                                  0                          0   \n",
       "2017-04-23                                  0                          0   \n",
       "...                                       ...                        ...   \n",
       "2019-08-23                                  0                          0   \n",
       "2019-08-24                                  0                          0   \n",
       "2019-08-25                                  0                          0   \n",
       "2019-08-26                                  0                          0   \n",
       "2019-08-27                                  0                          0   \n",
       "\n",
       "            amazonpreordersalesrevenue  maxappleprice  pagelength  \\\n",
       "todate                                                              \n",
       "2017-04-19                           0              0         0.0   \n",
       "2017-04-20                           0              0         0.0   \n",
       "2017-04-21                           0              0         0.0   \n",
       "2017-04-22                           0              0         0.0   \n",
       "2017-04-23                           0              0         0.0   \n",
       "...                                ...            ...         ...   \n",
       "2019-08-23                           0              0       395.0   \n",
       "2019-08-24                           0              0       395.0   \n",
       "2019-08-25                           0              0       395.0   \n",
       "2019-08-26                           0              0       395.0   \n",
       "2019-08-27                           0              0       395.0   \n",
       "\n",
       "            pricewassetbypublisher  barnesandnobledistributor  \\\n",
       "todate                                                          \n",
       "2017-04-19                     0.0                          0   \n",
       "2017-04-20                     0.0                          0   \n",
       "2017-04-21                     0.0                          0   \n",
       "2017-04-22                     0.0                          0   \n",
       "2017-04-23                     0.0                          0   \n",
       "...                            ...                        ...   \n",
       "2019-08-23                     0.0                          0   \n",
       "2019-08-24                     0.0                          0   \n",
       "2019-08-25                     0.0                          0   \n",
       "2019-08-26                     0.0                          0   \n",
       "2019-08-27                     0.0                          0   \n",
       "\n",
       "            appledistributor  \n",
       "todate                        \n",
       "2017-04-19                 0  \n",
       "2017-04-20                 0  \n",
       "2017-04-21                 0  \n",
       "2017-04-22                 0  \n",
       "2017-04-23                 0  \n",
       "...                      ...  \n",
       "2019-08-23                 0  \n",
       "2019-08-24                 0  \n",
       "2019-08-25                 0  \n",
       "2019-08-26                 0  \n",
       "2019-08-27                 0  \n",
       "\n",
       "[6527 rows x 105 columns]"
      ]
     },
     "execution_count": 50,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_ts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "todate\n",
       "2017-04-01    17641.452632\n",
       "2017-05-01    18001.534091\n",
       "2017-06-01    24639.817757\n",
       "2017-07-01    29045.850000\n",
       "2017-08-01    30261.399038\n",
       "2017-09-01    20314.926108\n",
       "2017-10-01    17164.796380\n",
       "2017-11-01    13248.792208\n",
       "2017-12-01    10178.643478\n",
       "2018-01-01    18722.591489\n",
       "2018-02-01    14001.924242\n",
       "2018-03-01    13854.420814\n",
       "2018-04-01    13719.264822\n",
       "2018-05-01    13901.817829\n",
       "2018-06-01    26775.158590\n",
       "2018-07-01    28918.100775\n",
       "2018-08-01    37939.872428\n",
       "2018-09-01    27664.678261\n",
       "2018-10-01    22173.231481\n",
       "2018-11-01    12560.775194\n",
       "2018-12-01     8090.334507\n",
       "2019-01-01    14895.531496\n",
       "2019-02-01    11761.343891\n",
       "2019-03-01    11307.252101\n",
       "2019-04-01    13245.938776\n",
       "2019-05-01    11444.924242\n",
       "2019-06-01    20409.722689\n",
       "2019-07-01    28880.601810\n",
       "2019-08-01    30420.716578\n",
       "Freq: MS, Name: totalrevenue, dtype: float64"
      ]
     },
     "execution_count": 51,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#average revenue for months based on entity:\n",
    "date_rev = df_ts['totalrevenue'].resample('MS').mean()\n",
    "date_rev"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "todate\n",
       "2019-01-01    14895.531496\n",
       "2019-02-01    11761.343891\n",
       "2019-03-01    11307.252101\n",
       "2019-04-01    13245.938776\n",
       "2019-05-01    11444.924242\n",
       "2019-06-01    20409.722689\n",
       "2019-07-01    28880.601810\n",
       "2019-08-01    30420.716578\n",
       "Freq: MS, Name: totalrevenue, dtype: float64"
      ]
     },
     "execution_count": 52,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "date_rev['2019':]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<function matplotlib.pyplot.show(*args, **kw)>"
      ]
     },
     "execution_count": 53,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x432 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "date_rev.plot(figsize=(15,6))\n",
    "plt.show\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Sales are lower towards the end pf each year and higher mid year around June-July\n",
    "The data is stationary"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAABDAAAALICAYAAACJhQBYAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy8QZhcZAAAgAElEQVR4nOzdd3iUxdrH8e+kkNASSAg1Cb2FDqEjKopgA8QGCoJYEIVjP8d27L52PRZEVBAFkWIXCzakSknonVCT0BICIYW03Xn/yIIRkbrJk/L7XNdeuzv7zOy9IWR372fmHmOtRURERERERESkOPNxOgARERERERERkVNRAkNEREREREREij0lMERERERERESk2FMCQ0RERERERESKPSUwRERERERERKTY83M6gOKmWrVqtl69ek6HISIiIiIiIlImxcbGJltrw45vVwLjOPXq1SMmJsbpMERERERERETKJGPMzhO1awmJiIiIiIiIiBR7SmCIiIiIiIiISLGnBIaIiIiIiIiIFHtKYIiIiIiIiIhIsacEhoiIiEgZsPNABnH705wOQ0RE5KwpgSEiIiJSyu1IzqD/2IVcNXYRuw5kOh2OiIjIWVECQ0RERKQUS83MZcSkZRjAGBjz6XJy8txOhyUiInLGlMAQERERKaVyXW5GfRJLwsEjvHdTNC9d05pVCam8+ONGp0MTERE5Y35OByAiIiIi3met5b9frWXR1gO8em0bOtYLAWBY17pMWLCdLg1C6R1Vw+EoRURETp9mYIiIiIiUQh/M3860ZfGMvrARV3cIP9b+yOXNaVkniAdmriLx0BEHIxQRETkzSmCIiIiIlDI/rdvL//2wgctb1eK+3k3+8liAny9vD26Py23516cryHWpHoaIiJQMSmCIiIiIlCJrE1O5e9pKWtcJ5pVr2+DjY/52TL1qFfm/ga2I3XmQ137e7ECUIiIiZ04JDBEREZFSYt/hLG79KIaqFfx5f1g05cv5/uOx/drUZnCnCMb9vpW5m5OKMEoREZGzowSGiIiISCmQmZPHrR/FkJaVy4ThHaleOfCUfZ64sgVNa1Tmvukr2Xc4qwiiFBEROXtKYIiIiIiUcG635b7pq1i3O5U3B7ejea2g0+oX6O/L2BvbkZnj4u5pK3C5bSFHKiIicvaUwBAREREp4V7+aRM/rtvL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\n",
      "text/plain": [
       "<Figure size 1080x720 with 4 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "rcParams['figure.figsize']=15,10\n",
    "d = sm.tsa.seasonal_decompose(date_rev, model ='additive')\n",
    "fig = d.plot()\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_rev_dt=date_rev.reset_index()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>todate</th>\n",
       "      <th>totalrevenue</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>2017-04-01</td>\n",
       "      <td>17641.452632</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>2017-05-01</td>\n",
       "      <td>18001.534091</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>2017-06-01</td>\n",
       "      <td>24639.817757</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>2017-07-01</td>\n",
       "      <td>29045.850000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>2017-08-01</td>\n",
       "      <td>30261.399038</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>5</td>\n",
       "      <td>2017-09-01</td>\n",
       "      <td>20314.926108</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6</td>\n",
       "      <td>2017-10-01</td>\n",
       "      <td>17164.796380</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>7</td>\n",
       "      <td>2017-11-01</td>\n",
       "      <td>13248.792208</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>8</td>\n",
       "      <td>2017-12-01</td>\n",
       "      <td>10178.643478</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>9</td>\n",
       "      <td>2018-01-01</td>\n",
       "      <td>18722.591489</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>10</td>\n",
       "      <td>2018-02-01</td>\n",
       "      <td>14001.924242</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>11</td>\n",
       "      <td>2018-03-01</td>\n",
       "      <td>13854.420814</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>12</td>\n",
       "      <td>2018-04-01</td>\n",
       "      <td>13719.264822</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>13</td>\n",
       "      <td>2018-05-01</td>\n",
       "      <td>13901.817829</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>14</td>\n",
       "      <td>2018-06-01</td>\n",
       "      <td>26775.158590</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>15</td>\n",
       "      <td>2018-07-01</td>\n",
       "      <td>28918.100775</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>16</td>\n",
       "      <td>2018-08-01</td>\n",
       "      <td>37939.872428</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>17</td>\n",
       "      <td>2018-09-01</td>\n",
       "      <td>27664.678261</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>18</td>\n",
       "      <td>2018-10-01</td>\n",
       "      <td>22173.231481</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>19</td>\n",
       "      <td>2018-11-01</td>\n",
       "      <td>12560.775194</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>20</td>\n",
       "      <td>2018-12-01</td>\n",
       "      <td>8090.334507</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>21</td>\n",
       "      <td>2019-01-01</td>\n",
       "      <td>14895.531496</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>22</td>\n",
       "      <td>2019-02-01</td>\n",
       "      <td>11761.343891</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>23</td>\n",
       "      <td>2019-03-01</td>\n",
       "      <td>11307.252101</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>24</td>\n",
       "      <td>2019-04-01</td>\n",
       "      <td>13245.938776</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>25</td>\n",
       "      <td>2019-05-01</td>\n",
       "      <td>11444.924242</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>26</td>\n",
       "      <td>2019-06-01</td>\n",
       "      <td>20409.722689</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>27</td>\n",
       "      <td>2019-07-01</td>\n",
       "      <td>28880.601810</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>28</td>\n",
       "      <td>2019-08-01</td>\n",
       "      <td>30420.716578</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       todate  totalrevenue\n",
       "0  2017-04-01  17641.452632\n",
       "1  2017-05-01  18001.534091\n",
       "2  2017-06-01  24639.817757\n",
       "3  2017-07-01  29045.850000\n",
       "4  2017-08-01  30261.399038\n",
       "5  2017-09-01  20314.926108\n",
       "6  2017-10-01  17164.796380\n",
       "7  2017-11-01  13248.792208\n",
       "8  2017-12-01  10178.643478\n",
       "9  2018-01-01  18722.591489\n",
       "10 2018-02-01  14001.924242\n",
       "11 2018-03-01  13854.420814\n",
       "12 2018-04-01  13719.264822\n",
       "13 2018-05-01  13901.817829\n",
       "14 2018-06-01  26775.158590\n",
       "15 2018-07-01  28918.100775\n",
       "16 2018-08-01  37939.872428\n",
       "17 2018-09-01  27664.678261\n",
       "18 2018-10-01  22173.231481\n",
       "19 2018-11-01  12560.775194\n",
       "20 2018-12-01   8090.334507\n",
       "21 2019-01-01  14895.531496\n",
       "22 2019-02-01  11761.343891\n",
       "23 2019-03-01  11307.252101\n",
       "24 2019-04-01  13245.938776\n",
       "25 2019-05-01  11444.924242\n",
       "26 2019-06-01  20409.722689\n",
       "27 2019-07-01  28880.601810\n",
       "28 2019-08-01  30420.716578"
      ]
     },
     "execution_count": 56,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_rev_dt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_features = df_rev_dt.copy()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create features for Reveneue (difference between the reveneus)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "metadata": {},
   "outputs": [],
   "source": [
    "#creating our feature:\n",
    "for i in range(1,13):\n",
    "    name = 'lag_' + str(i)\n",
    "    df_features[name] = df_features['totalrevenue'].shift(i)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_features=df_features.dropna().reset_index(drop=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>todate</th>\n",
       "      <th>totalrevenue</th>\n",
       "      <th>lag_1</th>\n",
       "      <th>lag_2</th>\n",
       "      <th>lag_3</th>\n",
       "      <th>lag_4</th>\n",
       "      <th>lag_5</th>\n",
       "      <th>lag_6</th>\n",
       "      <th>lag_7</th>\n",
       "      <th>lag_8</th>\n",
       "      <th>lag_9</th>\n",
       "      <th>lag_10</th>\n",
       "      <th>lag_11</th>\n",
       "      <th>lag_12</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>2018-04-01</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "      <td>17164.796380</td>\n",
       "      <td>20314.926108</td>\n",
       "      <td>30261.399038</td>\n",
       "      <td>29045.850000</td>\n",
       "      <td>24639.817757</td>\n",
       "      <td>18001.534091</td>\n",
       "      <td>17641.452632</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>2018-05-01</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "      <td>17164.796380</td>\n",
       "      <td>20314.926108</td>\n",
       "      <td>30261.399038</td>\n",
       "      <td>29045.850000</td>\n",
       "      <td>24639.817757</td>\n",
       "      <td>18001.534091</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>2018-06-01</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "      <td>17164.796380</td>\n",
       "      <td>20314.926108</td>\n",
       "      <td>30261.399038</td>\n",
       "      <td>29045.850000</td>\n",
       "      <td>24639.817757</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>2018-07-01</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "      <td>17164.796380</td>\n",
       "      <td>20314.926108</td>\n",
       "      <td>30261.399038</td>\n",
       "      <td>29045.850000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>2018-08-01</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "      <td>17164.796380</td>\n",
       "      <td>20314.926108</td>\n",
       "      <td>30261.399038</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>5</td>\n",
       "      <td>2018-09-01</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "      <td>17164.796380</td>\n",
       "      <td>20314.926108</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6</td>\n",
       "      <td>2018-10-01</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "      <td>17164.796380</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>7</td>\n",
       "      <td>2018-11-01</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "      <td>13248.792208</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>8</td>\n",
       "      <td>2018-12-01</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "      <td>10178.643478</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>9</td>\n",
       "      <td>2019-01-01</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "      <td>18722.591489</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>10</td>\n",
       "      <td>2019-02-01</td>\n",
       "      <td>11761.343891</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "      <td>14001.924242</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>11</td>\n",
       "      <td>2019-03-01</td>\n",
       "      <td>11307.252101</td>\n",
       "      <td>11761.343891</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "      <td>13854.420814</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>12</td>\n",
       "      <td>2019-04-01</td>\n",
       "      <td>13245.938776</td>\n",
       "      <td>11307.252101</td>\n",
       "      <td>11761.343891</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "      <td>13719.264822</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>13</td>\n",
       "      <td>2019-05-01</td>\n",
       "      <td>11444.924242</td>\n",
       "      <td>13245.938776</td>\n",
       "      <td>11307.252101</td>\n",
       "      <td>11761.343891</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "      <td>13901.817829</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>14</td>\n",
       "      <td>2019-06-01</td>\n",
       "      <td>20409.722689</td>\n",
       "      <td>11444.924242</td>\n",
       "      <td>13245.938776</td>\n",
       "      <td>11307.252101</td>\n",
       "      <td>11761.343891</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "      <td>26775.158590</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>15</td>\n",
       "      <td>2019-07-01</td>\n",
       "      <td>28880.601810</td>\n",
       "      <td>20409.722689</td>\n",
       "      <td>11444.924242</td>\n",
       "      <td>13245.938776</td>\n",
       "      <td>11307.252101</td>\n",
       "      <td>11761.343891</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "      <td>28918.100775</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>16</td>\n",
       "      <td>2019-08-01</td>\n",
       "      <td>30420.716578</td>\n",
       "      <td>28880.601810</td>\n",
       "      <td>20409.722689</td>\n",
       "      <td>11444.924242</td>\n",
       "      <td>13245.938776</td>\n",
       "      <td>11307.252101</td>\n",
       "      <td>11761.343891</td>\n",
       "      <td>14895.531496</td>\n",
       "      <td>8090.334507</td>\n",
       "      <td>12560.775194</td>\n",
       "      <td>22173.231481</td>\n",
       "      <td>27664.678261</td>\n",
       "      <td>37939.872428</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       todate  totalrevenue         lag_1         lag_2         lag_3  \\\n",
       "0  2018-04-01  13719.264822  13854.420814  14001.924242  18722.591489   \n",
       "1  2018-05-01  13901.817829  13719.264822  13854.420814  14001.924242   \n",
       "2  2018-06-01  26775.158590  13901.817829  13719.264822  13854.420814   \n",
       "3  2018-07-01  28918.100775  26775.158590  13901.817829  13719.264822   \n",
       "4  2018-08-01  37939.872428  28918.100775  26775.158590  13901.817829   \n",
       "5  2018-09-01  27664.678261  37939.872428  28918.100775  26775.158590   \n",
       "6  2018-10-01  22173.231481  27664.678261  37939.872428  28918.100775   \n",
       "7  2018-11-01  12560.775194  22173.231481  27664.678261  37939.872428   \n",
       "8  2018-12-01   8090.334507  12560.775194  22173.231481  27664.678261   \n",
       "9  2019-01-01  14895.531496   8090.334507  12560.775194  22173.231481   \n",
       "10 2019-02-01  11761.343891  14895.531496   8090.334507  12560.775194   \n",
       "11 2019-03-01  11307.252101  11761.343891  14895.531496   8090.334507   \n",
       "12 2019-04-01  13245.938776  11307.252101  11761.343891  14895.531496   \n",
       "13 2019-05-01  11444.924242  13245.938776  11307.252101  11761.343891   \n",
       "14 2019-06-01  20409.722689  11444.924242  13245.938776  11307.252101   \n",
       "15 2019-07-01  28880.601810  20409.722689  11444.924242  13245.938776   \n",
       "16 2019-08-01  30420.716578  28880.601810  20409.722689  11444.924242   \n",
       "\n",
       "           lag_4         lag_5         lag_6         lag_7         lag_8  \\\n",
       "0   10178.643478  13248.792208  17164.796380  20314.926108  30261.399038   \n",
       "1   18722.591489  10178.643478  13248.792208  17164.796380  20314.926108   \n",
       "2   14001.924242  18722.591489  10178.643478  13248.792208  17164.796380   \n",
       "3   13854.420814  14001.924242  18722.591489  10178.643478  13248.792208   \n",
       "4   13719.264822  13854.420814  14001.924242  18722.591489  10178.643478   \n",
       "5   13901.817829  13719.264822  13854.420814  14001.924242  18722.591489   \n",
       "6   26775.158590  13901.817829  13719.264822  13854.420814  14001.924242   \n",
       "7   28918.100775  26775.158590  13901.817829  13719.264822  13854.420814   \n",
       "8   37939.872428  28918.100775  26775.158590  13901.817829  13719.264822   \n",
       "9   27664.678261  37939.872428  28918.100775  26775.158590  13901.817829   \n",
       "10  22173.231481  27664.678261  37939.872428  28918.100775  26775.158590   \n",
       "11  12560.775194  22173.231481  27664.678261  37939.872428  28918.100775   \n",
       "12   8090.334507  12560.775194  22173.231481  27664.678261  37939.872428   \n",
       "13  14895.531496   8090.334507  12560.775194  22173.231481  27664.678261   \n",
       "14  11761.343891  14895.531496   8090.334507  12560.775194  22173.231481   \n",
       "15  11307.252101  11761.343891  14895.531496   8090.334507  12560.775194   \n",
       "16  13245.938776  11307.252101  11761.343891  14895.531496   8090.334507   \n",
       "\n",
       "           lag_9        lag_10        lag_11        lag_12  \n",
       "0   29045.850000  24639.817757  18001.534091  17641.452632  \n",
       "1   30261.399038  29045.850000  24639.817757  18001.534091  \n",
       "2   20314.926108  30261.399038  29045.850000  24639.817757  \n",
       "3   17164.796380  20314.926108  30261.399038  29045.850000  \n",
       "4   13248.792208  17164.796380  20314.926108  30261.399038  \n",
       "5   10178.643478  13248.792208  17164.796380  20314.926108  \n",
       "6   18722.591489  10178.643478  13248.792208  17164.796380  \n",
       "7   14001.924242  18722.591489  10178.643478  13248.792208  \n",
       "8   13854.420814  14001.924242  18722.591489  10178.643478  \n",
       "9   13719.264822  13854.420814  14001.924242  18722.591489  \n",
       "10  13901.817829  13719.264822  13854.420814  14001.924242  \n",
       "11  26775.158590  13901.817829  13719.264822  13854.420814  \n",
       "12  28918.100775  26775.158590  13901.817829  13719.264822  \n",
       "13  37939.872428  28918.100775  26775.158590  13901.817829  \n",
       "14  27664.678261  37939.872428  28918.100775  26775.158590  \n",
       "15  22173.231481  27664.678261  37939.872428  28918.100775  \n",
       "16  12560.775194  22173.231481  27664.678261  37939.872428  "
      ]
     },
     "execution_count": 60,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_features"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To understand how useful are lag features are to redicting revenues we use OLS linear Regression Model:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.8060152803425606"
      ]
     },
     "execution_count": 61,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model = sf.ols(formula='totalrevenue ~ lag_1 + lag_2 + lag_3 + lag_4 + lag_5 + lag_6 + lag_7+lag_8+lag_9+lag_10+lag_11+lag_12',data= df_features)\n",
    "model_fit= model.fit()\n",
    "reg =model_fit.rsquared_adj\n",
    "reg"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "These features account for 80% of variation. Good to preced to Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "metadata": {},
   "outputs": [],
   "source": [
    "#test and training:\n",
    "from sklearn.preprocessing import MinMaxScaler\n",
    "df_features = df_features.drop(['todate'], axis=1)\n",
    "training_data, testing_data = df_features[0:-6].values, df_features[-6:].values\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "metadata": {},
   "outputs": [],
   "source": [
    "scale = MinMaxScaler(feature_range=(-1,1))\n",
    "scale = scale.fit(training_data)\n",
    "training_date=training_data.reshape(training_data.shape[0], training_data.shape[1])\n",
    "training_scale = scale.transform(training_data)\n",
    "\n",
    "testing_data=testing_data.reshape(testing_data.shape[0], testing_data.shape[1])\n",
    "testing_scale = scale.transform(testing_data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 64,
   "metadata": {},
   "outputs": [],
   "source": [
    "#model:\n",
    "x_train, y_train = training_scale[:,1:], training_scale[:,0:1]\n",
    "x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])\n",
    "\n",
    "x_test, y_test = testing_scale[:,1:], testing_scale[:,0:1]\n",
    "x_test = x_test.reshape(x_test.shape[0], 1, x_test.shape[1])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/100\n",
      "11/11 [==============================] - 0s 34ms/step - loss: 0.3811\n",
      "Epoch 2/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.3815\n",
      "Epoch 3/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.3631\n",
      "Epoch 4/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.3457\n",
      "Epoch 5/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.3296\n",
      "Epoch 6/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.3147\n",
      "Epoch 7/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.3007\n",
      "Epoch 8/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2876\n",
      "Epoch 9/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2752\n",
      "Epoch 10/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2634\n",
      "Epoch 11/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2522\n",
      "Epoch 12/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2416\n",
      "Epoch 13/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2314\n",
      "Epoch 14/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2216\n",
      "Epoch 15/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2122\n",
      "Epoch 16/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.2032\n",
      "Epoch 17/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1945\n",
      "Epoch 18/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1862\n",
      "Epoch 19/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1782\n",
      "Epoch 20/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1706\n",
      "Epoch 21/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1632\n",
      "Epoch 22/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1562\n",
      "Epoch 23/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1494\n",
      "Epoch 24/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1429\n",
      "Epoch 25/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1367\n",
      "Epoch 26/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1307\n",
      "Epoch 27/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1251\n",
      "Epoch 28/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1196\n",
      "Epoch 29/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1144\n",
      "Epoch 30/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1094\n",
      "Epoch 31/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1046\n",
      "Epoch 32/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.1000\n",
      "Epoch 33/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0957\n",
      "Epoch 34/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0915\n",
      "Epoch 35/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0875\n",
      "Epoch 36/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0837\n",
      "Epoch 37/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0801\n",
      "Epoch 38/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0766\n",
      "Epoch 39/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0733\n",
      "Epoch 40/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0701\n",
      "Epoch 41/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0670\n",
      "Epoch 42/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0641\n",
      "Epoch 43/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0612\n",
      "Epoch 44/100\n",
      "11/11 [==============================] - 0s 1ms/step - loss: 0.0584\n",
      "Epoch 45/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0558\n",
      "Epoch 46/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0532\n",
      "Epoch 47/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0507\n",
      "Epoch 48/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0483\n",
      "Epoch 49/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0460\n",
      "Epoch 50/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0439\n",
      "Epoch 51/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0418\n",
      "Epoch 52/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0399\n",
      "Epoch 53/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0382\n",
      "Epoch 54/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0365\n",
      "Epoch 55/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0350\n",
      "Epoch 56/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0336\n",
      "Epoch 57/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0323\n",
      "Epoch 58/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0311\n",
      "Epoch 59/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0300\n",
      "Epoch 60/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0290\n",
      "Epoch 61/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0281\n",
      "Epoch 62/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0273\n",
      "Epoch 63/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0265\n",
      "Epoch 64/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0258\n",
      "Epoch 65/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0251\n",
      "Epoch 66/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0245\n",
      "Epoch 67/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0239\n",
      "Epoch 68/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0233\n",
      "Epoch 69/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0228\n",
      "Epoch 70/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0223\n",
      "Epoch 71/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0218\n",
      "Epoch 72/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0214\n",
      "Epoch 73/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0209\n",
      "Epoch 74/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0205\n",
      "Epoch 75/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0201\n",
      "Epoch 76/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0197\n",
      "Epoch 77/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0193\n",
      "Epoch 78/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0189\n",
      "Epoch 79/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0186\n",
      "Epoch 80/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0182\n",
      "Epoch 81/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0179\n",
      "Epoch 82/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0175\n",
      "Epoch 83/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0172\n",
      "Epoch 84/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0169\n",
      "Epoch 85/100\n",
      "11/11 [==============================] - 0s 1ms/step - loss: 0.0165\n",
      "Epoch 86/100\n",
      "11/11 [==============================] - 0s 1ms/step - loss: 0.0162\n",
      "Epoch 87/100\n",
      "11/11 [==============================] - 0s 1ms/step - loss: 0.0159\n",
      "Epoch 88/100\n",
      "11/11 [==============================] - 0s 1ms/step - loss: 0.0156\n",
      "Epoch 89/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0153\n",
      "Epoch 90/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0150\n",
      "Epoch 91/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0147\n",
      "Epoch 92/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0144\n",
      "Epoch 93/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0141\n",
      "Epoch 94/100\n",
      "11/11 [==============================] - 0s 1ms/step - loss: 0.0139\n",
      "Epoch 95/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0136\n",
      "Epoch 96/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0133\n",
      "Epoch 97/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0131\n",
      "Epoch 98/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0128\n",
      "Epoch 99/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0125\n",
      "Epoch 100/100\n",
      "11/11 [==============================] - 0s 2ms/step - loss: 0.0123\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<keras.callbacks.callbacks.History at 0x1564eb4d0>"
      ]
     },
     "execution_count": 65,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model = Sequential()\n",
    "model.add(LSTM(4, batch_input_shape=(1, x_train.shape[1],x_train.shape[2]), stateful =True))\n",
    "model.add(Dense(1))\n",
    "model.compile(loss='mean_squared_error', optimizer='adam')\n",
    "model.fit(x_train, y_train, epochs=100, batch_size=1,verbose=1,shuffle=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "metadata": {},
   "outputs": [],
   "source": [
    "y_pred =model.predict(x_test, batch_size=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[-0.7284365 ],\n",
       "       [-0.6722015 ],\n",
       "       [-0.6319945 ],\n",
       "       [-0.02267508],\n",
       "       [ 0.484564  ],\n",
       "       [ 0.948901  ]], dtype=float32)"
      ]
     },
     "execution_count": 67,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_pred"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 68,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[-0.7844578 ],\n",
       "       [-0.65456053],\n",
       "       [-0.77523339],\n",
       "       [-0.17456758],\n",
       "       [ 0.3930043 ],\n",
       "       [ 0.49619616]])"
      ]
     },
     "execution_count": 68,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_test"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 69,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[[-0.72843653 -0.75403241 -0.54403334 -1.35229312 -0.82838428 -0.13587485\n",
      "   0.25974501  1.96286371  0.86622371  0.65281254 -0.62921678 -0.64739686\n",
      "  -0.63393695]]\n",
      "[[-0.67220151 -0.7844578  -0.75403241 -0.81600951 -1.15044788 -0.82838428\n",
      "  -0.13587485  0.86622638  1.76468325  0.86622371  0.65281254 -0.62921678\n",
      "  -0.64739686]]\n",
      "[[-0.63199449 -0.65456053 -0.7844578  -1.06299919 -0.66018161 -1.15044788\n",
      "  -0.82838428  0.28014252  0.74139796  1.76468325  0.86622371  0.65281254\n",
      "  -0.62921678]]\n",
      "[[-0.02267508 -0.77523339 -0.65456053 -1.0987839  -0.88597764 -0.66018161\n",
      "  -1.15044788 -0.745763    0.19451616  0.74139796  1.76468325  0.86622371\n",
      "   0.65281254]]\n",
      "[[ 0.48456401 -0.17456758 -0.77523339 -0.94600568 -0.91869174 -0.88597764\n",
      "  -0.66018161 -1.22287828 -0.76276844  0.19451616  0.74139796  1.76468325\n",
      "   0.86622371]]\n",
      "[[ 0.948901    0.3930043  -0.17456758 -1.08793464 -0.77902309 -0.91869174\n",
      "  -0.88597764 -0.49658222 -1.20797036 -0.76276844  0.19451616  0.74139796\n",
      "   1.76468325]]\n"
     ]
    }
   ],
   "source": [
    "#inverse transformation:\n",
    "import numpy as np\n",
    "y_pred =y_pred.reshape(y_pred.shape[0], 1, y_pred.shape[1])\n",
    "pred_test_list=[]\n",
    "\n",
    "for i in range(0, len(y_pred)):\n",
    "    x= np.concatenate([y_pred[i], x_test[i]],axis=1)\n",
    "    print (x)\n",
    "           \n",
    "    pred_test_list.append(x)\n",
    "               "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 70,
   "metadata": {},
   "outputs": [],
   "source": [
    "pred_test_list =np.array(pred_test_list)\n",
    "pred_test_list = pred_test_list.reshape(pred_test_list.shape[0], pred_test_list.shape[2])\n",
    "\n",
    "pred_inverted = scale.inverse_transform(pred_test_list)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 71,
   "metadata": {},
   "outputs": [],
   "source": [
    "r_list =[]\n",
    "df_date=list(df_rev_dt[-7:].todate)\n",
    "df_rev =list(df_rev_dt[-7:].totalrevenue)\n",
    "\n",
    "for i in range(0, len(pred_inverted)):\n",
    "    result_dic ={}\n",
    "    result_dic['todate']=df_date[i+1]\n",
    "    result_dic['pred_value']= (pred_inverted[i][0] + df_rev[i] )\n",
    "    result_dic['pred_value']=result_dic['pred_value'].round().astype(int)\n",
    "    r_list.append(result_dic)\n",
    "final_df =pd.DataFrame(r_list)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "metadata": {},
   "outputs": [],
   "source": [
    "#final_df['pred_value']=final_df['pred_value'].round().astype(int)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 73,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>todate</th>\n",
       "      <th>pred_value</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>2019-03-01</td>\n",
       "      <td>23905</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>2019-04-01</td>\n",
       "      <td>24290</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>2019-05-01</td>\n",
       "      <td>26829</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>2019-06-01</td>\n",
       "      <td>34122</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>2019-07-01</td>\n",
       "      <td>50657</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>5</td>\n",
       "      <td>2019-08-01</td>\n",
       "      <td>66058</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      todate  pred_value\n",
       "0 2019-03-01       23905\n",
       "1 2019-04-01       24290\n",
       "2 2019-05-01       26829\n",
       "3 2019-06-01       34122\n",
       "4 2019-07-01       50657\n",
       "5 2019-08-01       66058"
      ]
     },
     "execution_count": 73,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "final_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 74,
   "metadata": {},
   "outputs": [],
   "source": [
    "#merge with y:\n",
    "df_pred = pd.merge(df_rev_dt, final_df, on =\"todate\", how='left')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 75,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "        <script type=\"text/javascript\">\n",
       "        window.PlotlyConfig = {MathJaxConfig: 'local'};\n",
       "        if (window.MathJax) {MathJax.Hub.Config({SVG: {font: \"STIX-Web\"}});}\n",
       "        if (typeof require !== 'undefined') {\n",
       "        require.undef(\"plotly\");\n",
       "        define('plotly', function(require, exports, module) {\n",
       "            /**\n",
       "* plotly.js v1.52.2\n",
       "* Copyright 2012-2020, Plotly, Inc.\n",
       "* All rights reserved.\n",
       "* Licensed under the MIT license\n",
       "*/\n",
       "        });\n",
       "        require(['plotly'], function(Plotly) {\n",
       "            window._Plotly = Plotly;\n",
       "        });\n",
       "        }\n",
       "        </script>\n",
       "        "
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.plotly.v1+json": {
       "config": {
        "linkText": "Export to plot.ly",
        "plotlyServerURL": "https://plot.ly",
        "showLink": false
       },
       "data": [
        {
         "name": "original",
         "type": "scatter",
         "x": [
          "2017-04-01T00:00:00",
          "2017-05-01T00:00:00",
          "2017-06-01T00:00:00",
          "2017-07-01T00:00:00",
          "2017-08-01T00:00:00",
          "2017-09-01T00:00:00",
          "2017-10-01T00:00:00",
          "2017-11-01T00:00:00",
          "2017-12-01T00:00:00",
          "2018-01-01T00:00:00",
          "2018-02-01T00:00:00",
          "2018-03-01T00:00:00",
          "2018-04-01T00:00:00",
          "2018-05-01T00:00:00",
          "2018-06-01T00:00:00",
          "2018-07-01T00:00:00",
          "2018-08-01T00:00:00",
          "2018-09-01T00:00:00",
          "2018-10-01T00:00:00",
          "2018-11-01T00:00:00",
          "2018-12-01T00:00:00",
          "2019-01-01T00:00:00",
          "2019-02-01T00:00:00",
          "2019-03-01T00:00:00",
          "2019-04-01T00:00:00",
          "2019-05-01T00:00:00",
          "2019-06-01T00:00:00",
          "2019-07-01T00:00:00",
          "2019-08-01T00:00:00"
         ],
         "y": [
          17641.452631578948,
          18001.534090909092,
          24639.817757009347,
          29045.85,
          30261.39903846154,
          20314.926108374384,
          17164.796380090498,
          13248.792207792209,
          10178.64347826087,
          18722.5914893617,
          14001.924242424242,
          13854.420814479638,
          13719.264822134388,
          13901.817829457364,
          26775.15859030837,
          28918.100775193798,
          37939.87242798354,
          27664.678260869565,
          22173.23148148148,
          12560.77519379845,
          8090.334507042254,
          14895.531496062993,
          11761.343891402716,
          11307.252100840336,
          13245.938775510203,
          11444.924242424242,
          20409.722689075632,
          28880.60180995475,
          30420.716577540108
         ]
        },
        {
         "name": "predicted",
         "type": "scatter",
         "x": [
          "2017-04-01T00:00:00",
          "2017-05-01T00:00:00",
          "2017-06-01T00:00:00",
          "2017-07-01T00:00:00",
          "2017-08-01T00:00:00",
          "2017-09-01T00:00:00",
          "2017-10-01T00:00:00",
          "2017-11-01T00:00:00",
          "2017-12-01T00:00:00",
          "2018-01-01T00:00:00",
          "2018-02-01T00:00:00",
          "2018-03-01T00:00:00",
          "2018-04-01T00:00:00",
          "2018-05-01T00:00:00",
          "2018-06-01T00:00:00",
          "2018-07-01T00:00:00",
          "2018-08-01T00:00:00",
          "2018-09-01T00:00:00",
          "2018-10-01T00:00:00",
          "2018-11-01T00:00:00",
          "2018-12-01T00:00:00",
          "2019-01-01T00:00:00",
          "2019-02-01T00:00:00",
          "2019-03-01T00:00:00",
          "2019-04-01T00:00:00",
          "2019-05-01T00:00:00",
          "2019-06-01T00:00:00",
          "2019-07-01T00:00:00",
          "2019-08-01T00:00:00"
         ],
         "y": [
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          23905,
          24290,
          26829,
          34122,
          50657,
          66058
         ]
        }
       ],
       "layout": {
        "template": {
         "data": {
          "bar": [
           {
            "error_x": {
             "color": "#2a3f5f"
            },
            "error_y": {
             "color": "#2a3f5f"
            },
            "marker": {
             "line": {
              "color": "#E5ECF6",
              "width": 0.5
             }
            },
            "type": "bar"
           }
          ],
          "barpolar": [
           {
            "marker": {
             "line": {
              "color": "#E5ECF6",
              "width": 0.5
             }
            },
            "type": "barpolar"
           }
          ],
          "carpet": [
           {
            "aaxis": {
             "endlinecolor": "#2a3f5f",
             "gridcolor": "white",
             "linecolor": "white",
             "minorgridcolor": "white",
             "startlinecolor": "#2a3f5f"
            },
            "baxis": {
             "endlinecolor": "#2a3f5f",
             "gridcolor": "white",
             "linecolor": "white",
             "minorgridcolor": "white",
             "startlinecolor": "#2a3f5f"
            },
            "type": "carpet"
           }
          ],
          "choropleth": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "type": "choropleth"
           }
          ],
          "contour": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "contour"
           }
          ],
          "contourcarpet": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "type": "contourcarpet"
           }
          ],
          "heatmap": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "heatmap"
           }
          ],
          "heatmapgl": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "heatmapgl"
           }
          ],
          "histogram": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "histogram"
           }
          ],
          "histogram2d": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "histogram2d"
           }
          ],
          "histogram2dcontour": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "histogram2dcontour"
           }
          ],
          "mesh3d": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "type": "mesh3d"
           }
          ],
          "parcoords": [
           {
            "line": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "parcoords"
           }
          ],
          "pie": [
           {
            "automargin": true,
            "type": "pie"
           }
          ],
          "scatter": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatter"
           }
          ],
          "scatter3d": [
           {
            "line": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatter3d"
           }
          ],
          "scattercarpet": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattercarpet"
           }
          ],
          "scattergeo": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattergeo"
           }
          ],
          "scattergl": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattergl"
           }
          ],
          "scattermapbox": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattermapbox"
           }
          ],
          "scatterpolar": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatterpolar"
           }
          ],
          "scatterpolargl": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatterpolargl"
           }
          ],
          "scatterternary": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatterternary"
           }
          ],
          "surface": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "surface"
           }
          ],
          "table": [
           {
            "cells": {
             "fill": {
              "color": "#EBF0F8"
             },
             "line": {
              "color": "white"
             }
            },
            "header": {
             "fill": {
              "color": "#C8D4E3"
             },
             "line": {
              "color": "white"
             }
            },
            "type": "table"
           }
          ]
         },
         "layout": {
          "annotationdefaults": {
           "arrowcolor": "#2a3f5f",
           "arrowhead": 0,
           "arrowwidth": 1
          },
          "coloraxis": {
           "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
           }
          },
          "colorscale": {
           "diverging": [
            [
             0,
             "#8e0152"
            ],
            [
             0.1,
             "#c51b7d"
            ],
            [
             0.2,
             "#de77ae"
            ],
            [
             0.3,
             "#f1b6da"
            ],
            [
             0.4,
             "#fde0ef"
            ],
            [
             0.5,
             "#f7f7f7"
            ],
            [
             0.6,
             "#e6f5d0"
            ],
            [
             0.7,
             "#b8e186"
            ],
            [
             0.8,
             "#7fbc41"
            ],
            [
             0.9,
             "#4d9221"
            ],
            [
             1,
             "#276419"
            ]
           ],
           "sequential": [
            [
             0,
             "#0d0887"
            ],
            [
             0.1111111111111111,
             "#46039f"
            ],
            [
             0.2222222222222222,
             "#7201a8"
            ],
            [
             0.3333333333333333,
             "#9c179e"
            ],
            [
             0.4444444444444444,
             "#bd3786"
            ],
            [
             0.5555555555555556,
             "#d8576b"
            ],
            [
             0.6666666666666666,
             "#ed7953"
            ],
            [
             0.7777777777777778,
             "#fb9f3a"
            ],
            [
             0.8888888888888888,
             "#fdca26"
            ],
            [
             1,
             "#f0f921"
            ]
           ],
           "sequentialminus": [
            [
             0,
             "#0d0887"
            ],
            [
             0.1111111111111111,
             "#46039f"
            ],
            [
             0.2222222222222222,
             "#7201a8"
            ],
            [
             0.3333333333333333,
             "#9c179e"
            ],
            [
             0.4444444444444444,
             "#bd3786"
            ],
            [
             0.5555555555555556,
             "#d8576b"
            ],
            [
             0.6666666666666666,
             "#ed7953"
            ],
            [
             0.7777777777777778,
             "#fb9f3a"
            ],
            [
             0.8888888888888888,
             "#fdca26"
            ],
            [
             1,
             "#f0f921"
            ]
           ]
          },
          "colorway": [
           "#636efa",
           "#EF553B",
           "#00cc96",
           "#ab63fa",
           "#FFA15A",
           "#19d3f3",
           "#FF6692",
           "#B6E880",
           "#FF97FF",
           "#FECB52"
          ],
          "font": {
           "color": "#2a3f5f"
          },
          "geo": {
           "bgcolor": "white",
           "lakecolor": "white",
           "landcolor": "#E5ECF6",
           "showlakes": true,
           "showland": true,
           "subunitcolor": "white"
          },
          "hoverlabel": {
           "align": "left"
          },
          "hovermode": "closest",
          "mapbox": {
           "style": "light"
          },
          "paper_bgcolor": "white",
          "plot_bgcolor": "#E5ECF6",
          "polar": {
           "angularaxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           },
           "bgcolor": "#E5ECF6",
           "radialaxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           }
          },
          "scene": {
           "xaxis": {
            "backgroundcolor": "#E5ECF6",
            "gridcolor": "white",
            "gridwidth": 2,
            "linecolor": "white",
            "showbackground": true,
            "ticks": "",
            "zerolinecolor": "white"
           },
           "yaxis": {
            "backgroundcolor": "#E5ECF6",
            "gridcolor": "white",
            "gridwidth": 2,
            "linecolor": "white",
            "showbackground": true,
            "ticks": "",
            "zerolinecolor": "white"
           },
           "zaxis": {
            "backgroundcolor": "#E5ECF6",
            "gridcolor": "white",
            "gridwidth": 2,
            "linecolor": "white",
            "showbackground": true,
            "ticks": "",
            "zerolinecolor": "white"
           }
          },
          "shapedefaults": {
           "line": {
            "color": "#2a3f5f"
           }
          },
          "ternary": {
           "aaxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           },
           "baxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           },
           "bgcolor": "#E5ECF6",
           "caxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           }
          },
          "title": {
           "x": 0.05
          },
          "xaxis": {
           "automargin": true,
           "gridcolor": "white",
           "linecolor": "white",
           "ticks": "",
           "title": {
            "standoff": 15
           },
           "zerolinecolor": "white",
           "zerolinewidth": 2
          },
          "yaxis": {
           "automargin": true,
           "gridcolor": "white",
           "linecolor": "white",
           "ticks": "",
           "title": {
            "standoff": 15
           },
           "zerolinecolor": "white",
           "zerolinewidth": 2
          }
         }
        },
        "title": {
         "text": "Revenue Prediction"
        }
       }
      },
      "text/html": [
       "<div>\n",
       "        \n",
       "        \n",
       "            <div id=\"27af908f-d723-479e-9149-a66592198d60\" class=\"plotly-graph-div\" style=\"height:525px; width:100%;\"></div>\n",
       "            <script type=\"text/javascript\">\n",
       "                require([\"plotly\"], function(Plotly) {\n",
       "                    window.PLOTLYENV=window.PLOTLYENV || {};\n",
       "                    \n",
       "                if (document.getElementById(\"27af908f-d723-479e-9149-a66592198d60\")) {\n",
       "                    Plotly.newPlot(\n",
       "                        '27af908f-d723-479e-9149-a66592198d60',\n",
       "                        [{\"name\": \"original\", \"type\": \"scatter\", \"x\": [\"2017-04-01T00:00:00\", \"2017-05-01T00:00:00\", \"2017-06-01T00:00:00\", \"2017-07-01T00:00:00\", \"2017-08-01T00:00:00\", \"2017-09-01T00:00:00\", \"2017-10-01T00:00:00\", \"2017-11-01T00:00:00\", \"2017-12-01T00:00:00\", \"2018-01-01T00:00:00\", \"2018-02-01T00:00:00\", \"2018-03-01T00:00:00\", \"2018-04-01T00:00:00\", \"2018-05-01T00:00:00\", \"2018-06-01T00:00:00\", \"2018-07-01T00:00:00\", \"2018-08-01T00:00:00\", \"2018-09-01T00:00:00\", \"2018-10-01T00:00:00\", \"2018-11-01T00:00:00\", \"2018-12-01T00:00:00\", \"2019-01-01T00:00:00\", \"2019-02-01T00:00:00\", \"2019-03-01T00:00:00\", \"2019-04-01T00:00:00\", \"2019-05-01T00:00:00\", \"2019-06-01T00:00:00\", \"2019-07-01T00:00:00\", \"2019-08-01T00:00:00\"], \"y\": [17641.452631578948, 18001.534090909092, 24639.817757009347, 29045.85, 30261.39903846154, 20314.926108374384, 17164.796380090498, 13248.792207792209, 10178.64347826087, 18722.5914893617, 14001.924242424242, 13854.420814479638, 13719.264822134388, 13901.817829457364, 26775.15859030837, 28918.100775193798, 37939.87242798354, 27664.678260869565, 22173.23148148148, 12560.77519379845, 8090.334507042254, 14895.531496062993, 11761.343891402716, 11307.252100840336, 13245.938775510203, 11444.924242424242, 20409.722689075632, 28880.60180995475, 30420.716577540108]}, {\"name\": \"predicted\", \"type\": \"scatter\", \"x\": [\"2017-04-01T00:00:00\", \"2017-05-01T00:00:00\", \"2017-06-01T00:00:00\", \"2017-07-01T00:00:00\", \"2017-08-01T00:00:00\", \"2017-09-01T00:00:00\", \"2017-10-01T00:00:00\", \"2017-11-01T00:00:00\", \"2017-12-01T00:00:00\", \"2018-01-01T00:00:00\", \"2018-02-01T00:00:00\", \"2018-03-01T00:00:00\", \"2018-04-01T00:00:00\", \"2018-05-01T00:00:00\", \"2018-06-01T00:00:00\", \"2018-07-01T00:00:00\", \"2018-08-01T00:00:00\", \"2018-09-01T00:00:00\", \"2018-10-01T00:00:00\", \"2018-11-01T00:00:00\", \"2018-12-01T00:00:00\", \"2019-01-01T00:00:00\", \"2019-02-01T00:00:00\", \"2019-03-01T00:00:00\", \"2019-04-01T00:00:00\", \"2019-05-01T00:00:00\", \"2019-06-01T00:00:00\", \"2019-07-01T00:00:00\", \"2019-08-01T00:00:00\"], \"y\": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 23905.0, 24290.0, 26829.0, 34122.0, 50657.0, 66058.0]}],\n",
       "                        {\"template\": {\"data\": {\"bar\": [{\"error_x\": {\"color\": \"#2a3f5f\"}, \"error_y\": {\"color\": \"#2a3f5f\"}, \"marker\": {\"line\": {\"color\": \"#E5ECF6\", \"width\": 0.5}}, \"type\": \"bar\"}], \"barpolar\": [{\"marker\": {\"line\": {\"color\": \"#E5ECF6\", \"width\": 0.5}}, \"type\": \"barpolar\"}], \"carpet\": [{\"aaxis\": {\"endlinecolor\": \"#2a3f5f\", \"gridcolor\": \"white\", \"linecolor\": \"white\", \"minorgridcolor\": \"white\", \"startlinecolor\": \"#2a3f5f\"}, \"baxis\": {\"endlinecolor\": \"#2a3f5f\", \"gridcolor\": \"white\", \"linecolor\": \"white\", \"minorgridcolor\": \"white\", \"startlinecolor\": \"#2a3f5f\"}, \"type\": \"carpet\"}], \"choropleth\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"type\": \"choropleth\"}], \"contour\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"contour\"}], \"contourcarpet\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"type\": \"contourcarpet\"}], \"heatmap\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"heatmap\"}], \"heatmapgl\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"heatmapgl\"}], \"histogram\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"histogram\"}], \"histogram2d\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"histogram2d\"}], \"histogram2dcontour\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"histogram2dcontour\"}], \"mesh3d\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"type\": \"mesh3d\"}], \"parcoords\": [{\"line\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"parcoords\"}], \"pie\": [{\"automargin\": true, \"type\": \"pie\"}], \"scatter\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatter\"}], \"scatter3d\": [{\"line\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatter3d\"}], \"scattercarpet\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattercarpet\"}], \"scattergeo\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattergeo\"}], \"scattergl\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattergl\"}], \"scattermapbox\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scattermapbox\"}], \"scatterpolar\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatterpolar\"}], \"scatterpolargl\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatterpolargl\"}], \"scatterternary\": [{\"marker\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"type\": \"scatterternary\"}], \"surface\": [{\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}, \"colorscale\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"type\": \"surface\"}], \"table\": [{\"cells\": {\"fill\": {\"color\": \"#EBF0F8\"}, \"line\": {\"color\": \"white\"}}, \"header\": {\"fill\": {\"color\": \"#C8D4E3\"}, \"line\": {\"color\": \"white\"}}, \"type\": \"table\"}]}, \"layout\": {\"annotationdefaults\": {\"arrowcolor\": \"#2a3f5f\", \"arrowhead\": 0, \"arrowwidth\": 1}, \"coloraxis\": {\"colorbar\": {\"outlinewidth\": 0, \"ticks\": \"\"}}, \"colorscale\": {\"diverging\": [[0, \"#8e0152\"], [0.1, \"#c51b7d\"], [0.2, \"#de77ae\"], [0.3, \"#f1b6da\"], [0.4, \"#fde0ef\"], [0.5, \"#f7f7f7\"], [0.6, \"#e6f5d0\"], [0.7, \"#b8e186\"], [0.8, \"#7fbc41\"], [0.9, \"#4d9221\"], [1, \"#276419\"]], \"sequential\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]], \"sequentialminus\": [[0.0, \"#0d0887\"], [0.1111111111111111, \"#46039f\"], [0.2222222222222222, \"#7201a8\"], [0.3333333333333333, \"#9c179e\"], [0.4444444444444444, \"#bd3786\"], [0.5555555555555556, \"#d8576b\"], [0.6666666666666666, \"#ed7953\"], [0.7777777777777778, \"#fb9f3a\"], [0.8888888888888888, \"#fdca26\"], [1.0, \"#f0f921\"]]}, \"colorway\": [\"#636efa\", \"#EF553B\", \"#00cc96\", \"#ab63fa\", \"#FFA15A\", \"#19d3f3\", \"#FF6692\", \"#B6E880\", \"#FF97FF\", \"#FECB52\"], \"font\": {\"color\": \"#2a3f5f\"}, \"geo\": {\"bgcolor\": \"white\", \"lakecolor\": \"white\", \"landcolor\": \"#E5ECF6\", \"showlakes\": true, \"showland\": true, \"subunitcolor\": \"white\"}, \"hoverlabel\": {\"align\": \"left\"}, \"hovermode\": \"closest\", \"mapbox\": {\"style\": \"light\"}, \"paper_bgcolor\": \"white\", \"plot_bgcolor\": \"#E5ECF6\", \"polar\": {\"angularaxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}, \"bgcolor\": \"#E5ECF6\", \"radialaxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}}, \"scene\": {\"xaxis\": {\"backgroundcolor\": \"#E5ECF6\", \"gridcolor\": \"white\", \"gridwidth\": 2, \"linecolor\": \"white\", \"showbackground\": true, \"ticks\": \"\", \"zerolinecolor\": \"white\"}, \"yaxis\": {\"backgroundcolor\": \"#E5ECF6\", \"gridcolor\": \"white\", \"gridwidth\": 2, \"linecolor\": \"white\", \"showbackground\": true, \"ticks\": \"\", \"zerolinecolor\": \"white\"}, \"zaxis\": {\"backgroundcolor\": \"#E5ECF6\", \"gridcolor\": \"white\", \"gridwidth\": 2, \"linecolor\": \"white\", \"showbackground\": true, \"ticks\": \"\", \"zerolinecolor\": \"white\"}}, \"shapedefaults\": {\"line\": {\"color\": \"#2a3f5f\"}}, \"ternary\": {\"aaxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}, \"baxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}, \"bgcolor\": \"#E5ECF6\", \"caxis\": {\"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\"}}, \"title\": {\"x\": 0.05}, \"xaxis\": {\"automargin\": true, \"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\", \"title\": {\"standoff\": 15}, \"zerolinecolor\": \"white\", \"zerolinewidth\": 2}, \"yaxis\": {\"automargin\": true, \"gridcolor\": \"white\", \"linecolor\": \"white\", \"ticks\": \"\", \"title\": {\"standoff\": 15}, \"zerolinecolor\": \"white\", \"zerolinewidth\": 2}}}, \"title\": {\"text\": \"Revenue Prediction\"}},\n",
       "                        {\"responsive\": true}\n",
       "                    ).then(function(){\n",
       "                            \n",
       "var gd = document.getElementById('27af908f-d723-479e-9149-a66592198d60');\n",
       "var x = new MutationObserver(function (mutations, observer) {{\n",
       "        var display = window.getComputedStyle(gd).display;\n",
       "        if (!display || display === 'none') {{\n",
       "            console.log([gd, 'removed!']);\n",
       "            Plotly.purge(gd);\n",
       "            observer.disconnect();\n",
       "        }}\n",
       "}});\n",
       "\n",
       "// Listen for the removal of the full notebook cells\n",
       "var notebookContainer = gd.closest('#notebook-container');\n",
       "if (notebookContainer) {{\n",
       "    x.observe(notebookContainer, {childList: true});\n",
       "}}\n",
       "\n",
       "// Listen for the clearing of the current output cell\n",
       "var outputEl = gd.closest('.output');\n",
       "if (outputEl) {{\n",
       "    x.observe(outputEl, {childList: true});\n",
       "}}\n",
       "\n",
       "                        })\n",
       "                };\n",
       "                });\n",
       "            </script>\n",
       "        </div>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "\n",
    "plot_pred =[go.Scatter(x = df_pred['todate'], y= df_pred['totalrevenue'], name ='original'),\n",
    "            go.Scatter(x = df_pred['todate'], y=df_pred['pred_value'] , name= 'predicted')]\n",
    "\n",
    "plot_layout =go.Layout(title='Revenue Prediction')\n",
    "fig = go.Figure(data=plot_pred, layout=plot_layout)\n",
    "pyoff.iplot(fig)\n",
    "\n",
    "#Screenshot of output is attached in Repo\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Our Figure shows the predicted revenue with the Original Revenue. we can see that its a pretty good prediction and overall sales for both Entities are expected to Increase"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}