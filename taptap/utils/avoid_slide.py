import execjs
import re

def run_avoid(response_text:str =None):
    requestInfo = re.findall("requestInfo='(.*?)'", response_text)[0]
    # todo: ��Դ���ҵ��ƹ���������, ��ɱ��ύ�ķ���
    '''function reform(data) {
        var form = document.createElement('form');
        var parsedUrl = parseURL(requestInfo.url);
        parsedUrl.search = addQuery(parsedUrl.search,data)
        var newUrl = combineUrl(parsedUrl);
        form.action = newUrl;
        form.method = "POST";
        form.innerHTML = parseFormQuery(requestInfo.data).join('');
        document.body.appendChild(form);
        form.submit();
        // document.body.appendChild(form);
    }'''