require 'rubygems'
require 'net/http'
require 'json'
require 'openssl'
# require 'date'
$proxy_host = 'dev-proxy.db.rakuten.co.jp'
$proxy_port = '8301'
$jira_bot = ENV['USER']
puts 'Password'
$bot_pass = gets.chomp

=begin
def notify_slack(message)
        slackApiKey='xxxxxxxxxx';
        slack_api = "https://slack.com/api/chat.postMessage?token=#{slackApiKey}&channel=bot_log_notify&text=#{message}&as_user=true";
        encoded_url = URI.encode(slack_api)
        uri = URI.parse(encoded_url)
#               http = Net::HTTP.new(uri.host, uri.port)
        http = Net::HTTP.new(uri.host, uri.port, $proxy_host, $proxy_port)
        http.use_ssl = true
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE
        request = Net::HTTP::Get.new(uri.request_uri)
        response = http.request(request)
        if response.code =~ /20[0-9]{1}/
        return true
        else
        raise StandardError, "Unsuccessful response code " + response.code + " for issue "
                return false
        end
end

=end




def close(key)
        url = "https://jira.rakuten-it.com/jira/rest/api/2/issue/#{key}/transitions"
        # https://jira.rakuten-it.com/jira/rest/api/2/issue/SVRADM-9600/transitions
        data = {
                "update" => {
                "comment" => [{
                        "add" => {
                                "body" => "This ticket’s status hasn’t changed in the last three days, so we will change the status to “closed”.\n
                                If you need anything else, please raise a new request.\n
                                https://confluence.rakuten-it.com/confluence/display/id/ID+Client+Support+Ticket+Creation\n
                                Sorry for the inconvenience\n
                                Best regards,\n
                                Operation Support Team"
                                }
                        }]
                },
        "transition" => {
                "id" => "701"
        }
        }.to_json
        uri = URI.parse(url)
#               http = Net::HTTP.new(uri.host, uri.port)
        http = Net::HTTP.new(uri.host, uri.port, $proxy_host, $proxy_port)
        http.use_ssl = true
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE
        request = Net::HTTP::Post.new(uri.path)
        request.basic_auth $jira_bot, $bot_pass
        request["Content-Type"] = "application/json"
        request.body = data
        response = http.request(request)
        if response.code =~ /20[0-9]{1}/
                message = "Successfully closed https://jira.rakuten-it.com/jira/browse/IDCS."
#                       notify_slack(message)
        return true
        else
                message = "Failed to close https://jira.rakuten-it.com/jira/browse/IDCS."
#                       notify_slack(message)
        raise StandardError, "Unsuccessful response code " + response.code + " for issue "
                return false
        end
end

jira_url = "https://jira.rakuten-it.com/jira/rest/api/2/search?jql=filter%3D195443"
uri = URI.parse(jira_url)
#http = Net::HTTP.new(uri.host, uri.port)
http = Net::HTTP.new(uri.host, uri.port, $proxy_host, $proxy_port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE
request = Net::HTTP::Get.new(uri.request_uri)
request.basic_auth $jira_bot, $bot_pass
request["Content-Type"] = "application/json"
response = http.request(request)
if response.code =~ /20[0-9]{1}/
#               notify_slack(" ---  Start close tickets in https://jira.rakuten-it.com/jira/issues/?filter=62102  ---")
        data = JSON.parse(response.body)
        if data['total'] < 1
                puts 'No tickets to close'
#                       notify_slack("---  No tiket to close  ---")
                exit
        end
        data['issues'].each do |issue|
                key = issue['key']
#               notify_slack("confirming https://jira.rakuten-it.com/jira/browse/#{key}")
                close(key)
                sleep(5)
        end
                puts 'Successfully done'
#               notify_slack("---  Finish  ---")
else
        raise StandardError, "Unsuccessful response code " + response.code + " for issue "
end
