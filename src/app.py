import numpy, dash, math
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

server = app.server

ColorWay = ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52",
            "#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52",
            "#636efa", "#EF553B"]

nVLabel = {0: '0', 5: '5', 10: '10', 15: '15', 20: '20'}

app.layout = html.Div([
    html.H1('Quantum Harmonic Oscillator',style={'font-family': 'sans-serif',"margin-top": "20","margin-bottom": "10", 'padding-left': '2.5%','padding-right': '2.5%'}),
    html.Div([
        html.Div([html.Div(html.H5('Range Of Eigenstates',style={'font-family': 'sans-serif','textAlign': 'center'}),id='max_v_lab'),
                dcc.RangeSlider(id='v_max',min=0,max=20,step=1,value=[0,5],marks=nVLabel,updatemode='drag',tooltip=dict(always_visible=False,placement='bottom'),dots=False)],style={'width': '80%', 'display': 'inline-block', 'padding-left': '10%','padding-right': '10%'})
        ],style={'width': '100%', 'display': 'inline-block','vertical-align': 'middle'}),
        html.Br(),html.Br(),
        html.Div([
            html.Div([html.H5('Wavefunction ψ',style={'font-family': 'sans-serif',"margin-top": "10","margin-bottom": "5",'textAlign': 'center'}),dcc.Graph(id='qho_psi',config={'displayModeBar': False})],style={'width': '45%', 'padding-left': '2.5%','padding-right': '2.5%', 'display': 'inline-block'}),
            html.Div([html.H5('Probability Density |ψ|²',style={'font-family': 'sans-serif',"margin-top": "10","margin-bottom": "5",'textAlign': 'center'}),dcc.Graph(id='qho_psi2',config={'displayModeBar': False})],style={'width': '45%', 'padding-left': '2.5%','padding-right': '2.5%', 'display': 'inline-block'})
        ],style={'width': '100%', 'display': 'inline-block','vertical-align': 'middle'})
])

@app.callback(
    Output('qho_psi', 'figure'),
    [Input('v_max'  , 'value')])
def UpdateWfn(vrng):
    vmin, vmax = vrng[0], vrng[1]
    HerV = HermitePoly(vmax)
    qmin = -1.10 * numpy.sqrt(2.0*vmax+1.0)
    qmax =  1.25 * numpy.sqrt(2.0*vmax+1.0)
    q = numpy.linspace(qmin,qmax,num=501)
    w = numpy.zeros((501))
    Vofq = 0.5 * q * q
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q,y=Vofq,mode='lines',line_shape='spline',line_color='black',line_width=1.0,name='V(q)',hoverinfo='name'))
    for v in range(vmin,vmax+1):
        w[:] = 1.0*v + 0.5
        Phi = 0.7*HarmonicWfn(v,q,HerV[v]) + w
        fig.add_trace(go.Scatter(x=q,y=w,mode='lines',line_shape='spline',line_width=1.0,line_dash='dash',line_color='black',name='{0:.1f}&#8463;&#969;'.format(v+0.5),hoverinfo='none'))
        fig.add_trace(go.Scatter(x=q,y=Phi,mode='lines',line_shape='spline',line_width=2.0,name='&#968;<sub>{0:d}</sub>'.format(v),hoverinfo='name',fill='tonexty',line_color=ColorWay[v]))
        fig.add_annotation(x=0.0,y=w[0],xref="paper",yref="y",text="{0:.1f}&#8463;&#969;".format(v+0.5),showarrow=False)
        
    fig.update_layout(template='plotly_white',margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},hovermode='closest',autosize=True,legend=dict(orientation='h',yanchor='middle',y=1.0,xanchor='center',x=0.5,bgcolor="rgba(0,0,0,0)",font=dict(size=12)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(title='q',tickformat = 'd',showgrid=False,showline=True,linewidth=2,linecolor='black',ticks="outside",tickwidth=2,ticklen=6,title_font=dict(size=12),tickfont=dict(size=10),range=[-1.08*qmax,1.08*qmax]),yaxis=dict(tickformat = 'd',showgrid=False,showline=True,linewidth=2,linecolor='black',anchor='free',position=0.5,ticks="outside",tickwidth=2,ticklen=0,title_font=dict(size=12),tickfont=dict(size=10),showticklabels=False,range=[max(0,vmin),vmax+1]),showlegend=False) 
    return fig

@app.callback(
    Output('qho_psi2','figure'),
    [Input('v_max'  , 'value')])
def UpdateWf2(vrng):
    vmin, vmax = vrng[0], vrng[1]
    HerV = HermitePoly(vmax)
    qmin = -1.10 * numpy.sqrt(2.0*vmax+1.0)
    qmax =  1.25 * numpy.sqrt(2.0*vmax+1.0)
    q = numpy.linspace(qmin,qmax,num=501)
    w = numpy.zeros((501))
    Vofq = 0.5 * q * q
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q,y=Vofq,mode='lines',line_shape='spline',line_color='black',line_width=1.0,name='V(q)',hoverinfo='name'))
    for v in range(vmin,vmax+1):
        w[:] = 1.0*v + 0.5
        Phi = HarmonicWfn(v,q,HerV[v])
        Phi2 = (1.0 * Phi * Phi) + w
        fig.add_trace(go.Scatter(x=q,y=w,mode='lines',line_shape='spline',line_width=1.0,line_dash='dash',line_color='black',name='{0:.1f}&#8463;&#969;'.format(v+0.5),hoverinfo='none'))
        fig.add_trace(go.Scatter(x=q,y=Phi2,mode='lines',line_shape='spline',line_width=2.0,name='|&#968;<sub>{0:d}</sub>|<sup>2</sup>'.format(v),hoverinfo='name',fill='tonexty',line_color=ColorWay[v]))
        fig.add_annotation(x=0.0,y=w[0],xref="paper",yref="y",text="{0:.1f}&#8463;&#969;".format(v+0.5),showarrow=False)
        
    fig.update_layout(template='plotly_white',margin={'t': 0, 'l': 0, 'r': 0, 'b': 0},hovermode='closest',autosize=True,legend=dict(orientation='h',yanchor='middle',y=1.0,xanchor='center',x=0.5,bgcolor="rgba(0,0,0,0)",font=dict(size=12)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(title='q',tickformat = 'd',showgrid=False,showline=True,linewidth=2,linecolor='black',ticks="outside",tickwidth=2,ticklen=6,title_font=dict(size=12),tickfont=dict(size=10),range=[-1.08*qmax,1.08*qmax]),yaxis=dict(tickformat = 'd',showgrid=False,showline=True,linewidth=2,linecolor='black',anchor='free',position=0.5,ticks="outside",tickwidth=2,ticklen=0,title_font=dict(size=12),tickfont=dict(size=10),showticklabels=False,range=[max(0,vmin),vmax+1]),showlegend=False) 
    return fig

def HermitePoly(n):
    Hn = []
    Hn.append(numpy.poly1d([1.0]))
    Hn.append(numpy.poly1d([2.0,0.0]))
    for v in range(2,n+1):
        Hn.append(Hn[1]*Hn[v-1] - 2.0*(v-1)*Hn[v-2])
    return Hn

def HarmonicWfn(v,q,Hv):
    Nrm = 1.0 / numpy.sqrt(pow(2.0,v)*math.factorial(v)*numpy.sqrt(numpy.pi))
    Wfn = Nrm * Hv(q) * numpy.exp(-0.5*q*q)
    return Wfn
    
if __name__ == '__main__':
    app.run_server(debug=False)