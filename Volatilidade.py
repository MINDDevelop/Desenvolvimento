import xml.etree.ElementTree as ET
arquivo_xml = r"C:\Users\vgonçalves\Documents\SPRD240122\BVBG.187.01_BV000471202401220001000072001359930.xml"
tree = ET.parse(arquivo_xml)
root = tree.getroot()

# Itere sobre os elementos
for biz_grp in root.findall('.//BizGrp'):
    # Obter informações do AppHdr
    app_hdr = biz_grp.find('.//AppHdr')
    biz_msg_idr = app_hdr.find('.//BizMsgIdr').text
    msg_def_idr = app_hdr.find('.//MsgDefIdr').text
    cre_dt = app_hdr.find('.//CreDt').text

    # Obter informações do Document
    document = biz_grp.find('.//Document')
    trad_dt = document.find('.//TradDt/Dt').text
    tckr_symb = document.find('.//SctyId/TckrSymb').text
    opn_intrst = document.find('.//FinInstrmAttrbts/OpnIntrst').text
    last_pric = document.find('.//FinInstrmAttrbts/LastPric').text

    # Imprimir as informações
    print(f"BizMsgIdr: {biz_msg_idr}")
    print(f"MsgDefIdr: {msg_def_idr}")
    print(f"CreDt: {cre_dt}")
    print(f"TradDt: {trad_dt}")
    print(f"TckrSymb: {tckr_symb}")
    print(f"OpnIntrst: {opn_intrst}")
    print(f"LastPric: {last_pric}")
    print("\n" + "-"*30 + "\n")