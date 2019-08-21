#! /usr/bin/ruby

require 'pry'
require 'aws-sdk-ec2'
require 'net/http'

group_name = 'home'

# Get my public IP address
begin
  public_ip = Net::HTTP.get(URI('https://api.ipify.org'))
rescue
  raise 'Could not get public IP address!'
  exit 1
end

ec2 = Aws::EC2::Client.new

# Find all current rules
current = ec2.describe_security_groups({group_names: [group_name] })['security_groups']
raise 'Too many security groups matched!' if current.count > 1
raise 'Could not find security group!' if current.count < 1
current = current[0].to_h

# Remove any empty values as *_security_group_ingress doesn't like it
current[:ip_permissions].each {|a| a.delete_if {|k,v| v.empty? if v.is_a?(Array) } }

# Swap any current inbound IPs with my current public IP
new_rules = Marshal.load(Marshal.dump(current))
new_rules[:ip_permissions].each do |perm|
  perm[:ip_ranges].each {|a| a[:cidr_ip] = public_ip + '/32'}
end

# Add new rules
ec2.authorize_security_group_ingress({
  group_name: group_name,
  ip_permissions: new_rules[:ip_permissions]
})

# Remove all other rules wihtout my IP
ec2.revoke_security_group_ingress({
  group_name: group_name,
  ip_permissions: current[:ip_permissions]
})
