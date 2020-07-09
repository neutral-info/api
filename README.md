# api


## 開發環境設定

- pipenv shell: 啟動虛擬環境
- pipenv sync: 同步 package
- pipenv install -e .: 把 project 變成 package (主要是為了將 project 路徑新增到 pythonpath)

## run api server

- pipenv run uvicorn api.main:app --reload --host 0.0.0.0

- url: http://127.0.0.1:8000/docs

## future work

- todo list
    - keywords, producer_position:修改成 dict
    ''' exapmle
        {
            partyName: '民進黨‘,
            value: 0.65
        },

        {
            id: 'test',
            publicData: '2020-09-11',
            title: 'test',
            content: 'test',
            keywords: ['test', ' test', 'test',']
            producer: {
                id: 'tes',
                description: 'test',
                postions: [
                    {
                    party: 'test',
                    value: 'test
                    },
                ]
            }
        }
    '''
- dockerize
