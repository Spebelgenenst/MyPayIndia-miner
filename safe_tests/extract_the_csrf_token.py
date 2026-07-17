input = """
         const clickBatchSize = 10;
            const payout_every = 100;
            const csrfToken = "********";
            let total_clicks = 4510180;
            let payout_in = 20;
            const root = document.querySelector(':root');
"""
search = "const csrfToken = \""
csrf_token_location = input.find(search)
print(csrf_token_location)

start = csrf_token_location + len(search)

print(start)
print(input[start:start+40])